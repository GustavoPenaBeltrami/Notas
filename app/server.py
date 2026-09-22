#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "mlx-whisper; sys_platform == 'darwin' and platform_machine == 'arm64'",
#   "faster-whisper; (sys_platform != 'darwin' or platform_machine != 'arm64') and (sys_platform != 'win32' or platform_machine != 'ARM64')",
# ]
# ///
"""Servidor local del sistema de estudio. Solo stdlib: python3 app/server.py

El dictado es lo unico que necesita algo mas: mlx-whisper en Mac Apple Silicon,
faster-whisper en el resto. `npm run app` (uv run) trae el que corresponde;
sin eso todo anda igual menos el microfono.
"""
import base64, datetime, hashlib, http.server, json, os, pathlib, re, sys, threading, urllib.parse, webbrowser

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import texto

RAIZ = pathlib.Path(__file__).resolve().parent.parent
TEMAS = RAIZ / "temas"
PUERTO = 8321
MODELO_VOZ = "mlx-community/whisper-large-v3-turbo"   # ~1,6 GB, se baja la primera vez
CPU_VOICE_MODEL = os.environ.get("NOTAS_MODELO_VOZ", "small")   # ponytail: CPU int8 only, set NOTAS_MODELO_VOZ=turbo on a fast box; CUDA needs device="auto" + cuDNN
candado_voz = threading.Lock()
cpu_model = None
LIMITE_CUERPO = 20 * 1024 * 1024   # ponytail: cap parejo para todo POST, un solo usuario local
EXT_AUDIO = {"audio/webm": "webm", "audio/ogg": "ogg", "audio/mp4": "mp4",
             "audio/wav": "wav", "audio/x-wav": "wav"}


def ext_audio(mime):
    """mime del MediaRecorder ('audio/webm;codecs=opus' -> 'webm'). Rechaza lo que no está en la whitelist."""
    ext = EXT_AUDIO.get(mime.split(";")[0].strip().lower())
    if not ext:
        raise ValueError("tipo de audio no permitido: " + mime)
    return ext


def whisper(audio, idioma):
    global cpu_model
    try:
        import mlx_whisper
    except ImportError:
        mlx_whisper = None
    if mlx_whisper:
        r = mlx_whisper.transcribe(audio, path_or_hf_repo=MODELO_VOZ, language=idioma)
        return [[s["start"], s["text"].strip()] for s in r["segments"]]
    try:
        import faster_whisper
    except ImportError:
        raise ValueError("falta el motor de dictado, arranca con npm run app")
    if cpu_model is None:
        cpu_model = faster_whisper.WhisperModel(CPU_VOICE_MODEL, device="cpu", compute_type="int8")
    segments, _ = cpu_model.transcribe(audio, language=idioma)
    return [[s.start, s.text.strip()] for s in segments]


def transcribir(crudo):
    """float32 mono a 16 kHz, tal cual lo manda el navegador."""
    try:
        import numpy   # aca adentro: el resto del server no lo necesita
    except ImportError:
        raise ValueError("falta el motor de dictado, arranca con npm run app")
    with candado_voz:   # ponytail: una transcripcion a la vez, hay un solo usuario
        segmentos = whisper(numpy.frombuffer(crudo, dtype="<f4"), "es")
    # segmentos [inicio_s, texto]: el dictado en vivo fija los viejos y recorta el audio ahi
    return {"texto": " ".join(t for _, t in segmentos).strip(), "segmentos": segmentos}


def carpeta(slug):
    """Carpeta del tema. Rechaza cualquier cosa que se escape de temas/."""
    d = (TEMAS / slug).resolve()
    if d.parent != TEMAS or not d.is_dir():
        raise ValueError("tema inexistente: " + slug)
    return d


TIPOS = ("libro", "certificación", "documentación", "curso")


def meta(d):
    """Lo que describe al tema. `orden` manda en las listas; sin el, va al final."""
    archivo = d / "tema.json"
    guardado = json.loads(archivo.read_text()) if archivo.exists() else {}
    titulo = d.name if " " in d.name else d.name.replace("-", " ").capitalize()
    return {"titulo": guardado.get("titulo") or titulo,
            "subtitulo": guardado.get("subtitulo", ""),
            "tipo": guardado.get("tipo", "libro"),
            "orden": guardado.get("orden", 999),
            "enlaces": guardado.get("enlaces", [])}


def recursos(d):
    """PDFs, apuntes sueltos, lo que dejes en recursos/. Se sirven tal cual."""
    carpeta_r = d / "recursos"
    if not carpeta_r.is_dir():
        return []
    return [{"nombre": f.name,
             "ruta": f"/temas/{urllib.parse.quote(d.name)}/recursos/{urllib.parse.quote(f.name)}",
             "kb": round(f.stat().st_size / 1024)}
            for f in sorted(carpeta_r.iterdir()) if f.is_file() and not f.name.startswith(".")]


def ordenar(lista):
    return sorted(lista, key=lambda l: (l["orden"], texto.slug(l["titulo"])))


EXT = {"png": ".png", "jpeg": ".jpg", "jpg": ".jpg", "gif": ".gif",
       "webp": ".webp", "avif": ".avif", "svg+xml": ".svg"}
NOMBRE_IMG = re.compile(r"^[0-9a-f]{16}\.[a-z]+$")


def carpeta_img(slug):
    return TEMAS / slug / "notas" / "img"


def a_url(html, slug):
    """notas/img/x.png -> URL que el navegador puede pedir."""
    return html.replace('src="img/', f'src="/temas/{urllib.parse.quote(slug)}/notas/img/')


def a_ruta(html, slug):
    return html.replace(f'src="/temas/{urllib.parse.quote(slug)}/notas/img/', 'src="img/')


def extraer_imagenes(html, destino):
    """Saca las imagenes pegadas del .md y las deja como archivo aparte.

    El nombre es el hash del contenido: pegar dos veces la misma captura no
    duplica el archivo, y el .md queda con una referencia corta en vez de
    cientos de KB de base64.
    """
    def guardar(m):
        crudo = base64.b64decode(m.group(2))
        nombre = hashlib.sha1(crudo).hexdigest()[:16] + EXT.get(m.group(1), ".bin")
        destino.mkdir(parents=True, exist_ok=True)
        archivo = destino / nombre
        if not archivo.exists():
            archivo.write_bytes(crudo)
        return f'src="img/{nombre}"'

    return re.sub(r'src="data:image/([a-z+]+);base64,([^"]+)"', guardar, html)


def secciones(d):
    return sorted((d / "notas").glob("*.md"))


def titulos(d):
    return [re.sub(r"<[^>]+>|[*_~`\[\]]", "", l[2:]).strip()
            for f in secciones(d) for l in f.read_text().splitlines() if l.startswith("# ")]


def temas():
    salida = [{"slug": d.name, **meta(d), "secciones": len(secciones(d)),
               "recursos": len(recursos(d)), "indice": titulos(d)}
              for d in TEMAS.glob("*") if d.is_dir()]
    return ordenar(salida)


def leer_tema(slug):
    d = carpeta(slug)
    partes = [texto.md_a_html(f.read_text()) for f in secciones(d)]
    return {"slug": slug, **meta(d), "recursos": recursos(d),
            "html": a_url("\n".join(partes), slug)}


def guardar_tema(slug, datos):
    d = carpeta(slug)
    notas = d / "notas"
    notas.mkdir(exist_ok=True)
    actual = meta(d)                       # conserva `orden`, que no viaja en el editor
    actual.update({k: datos[k] for k in ("titulo", "subtitulo") if k in datos})
    (d / "tema.json").write_text(json.dumps(actual, ensure_ascii=False, indent=2) + "\n")

    html = extraer_imagenes(a_ruta(datos.get("html", ""), slug), notas / "img")
    usadas = set(re.findall(r'src="img/([^"]+)"', html))   # antes de partir: html se reusa abajo

    escritos = set()
    for i, (titulo, trozo) in enumerate(texto.partir_por_h1(html), 1):
        nombre = f"{i:02d}-{texto.slug(titulo)}.md"
        (notas / nombre).write_text(texto.html_a_md(trozo))
        escritos.add(nombre)
    for viejo in notas.glob("*.md"):          # secciones borradas o renombradas
        if viejo.name not in escritos:
            viejo.unlink()

    # imagenes que ya no referencia ningun .md. Solo las que genero el servidor,
    # por si alguna vez dejas un archivo tuyo en esa carpeta.
    img = notas / "img"
    if img.is_dir():
        for f in img.iterdir():
            if f.is_file() and f.name not in usadas and NOMBRE_IMG.match(f.name):
                f.unlink()
    return {"ok": True, "secciones": sorted(escritos)}


def indice_examenes():
    salida = [{"slug": d.name, **meta(d),
               "examenes": [{"ruta": f"temas/{d.name}/examenes/{f.parent.name}/examen.json",
                             "titulo": json.loads(f.read_text()).get("titulo", f.parent.name)}
                            for f in sorted((d / "examenes").glob("*/examen.json"))]}
              for d in TEMAS.glob("*") if d.is_dir()]
    return {"temas": ordenar(salida)}


def carpeta_examen(d, examen):
    """Carpeta del examen dentro del tema. Mismo chequeo de escape que carpeta()."""
    c = (d / "examenes" / examen).resolve()
    if c.parent != (d / "examenes").resolve() or not (c / "examen.json").is_file():
        raise ValueError("examen inexistente: " + examen)
    return c


def guardar_intento(slug, examen, respuestas):
    """Escribe examenes/<examen>/intentos/<fecha-a-minuto>.json. Devuelve la ruta relativa.

    Las respuestas orales con audio se guardan como archivo aparte
    (intentos/<fecha>-p<i>.<ext>); el JSON se queda con el nombre, no el base64.
    """
    c = carpeta_examen(carpeta(slug), examen)
    intentos = c / "intentos"
    intentos.mkdir(exist_ok=True)
    fecha = datetime.datetime.now().strftime("%Y-%m-%dT%H%M")
    for r in respuestas:
        if r.get("tipo") == "oral" and "audio" in r:
            ext = ext_audio(r.pop("mime", ""))
            nombre = f"{fecha}-p{r['i']}.{ext}"
            (intentos / nombre).write_bytes(base64.b64decode(r.pop("audio")))
            r["audio"] = nombre
    ruta = intentos / (fecha + ".json")
    ruta.write_text(json.dumps({"examen": examen, "respuestas": respuestas}, ensure_ascii=False, indent=2) + "\n")
    return str(ruta.relative_to(RAIZ))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(RAIZ), **kw)

    def responder(self, codigo, datos):
        cuerpo = json.dumps(datos, ensure_ascii=False).encode()
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(cuerpo)

    def do_GET(self):
        ruta = urllib.parse.unquote(self.path.split("?")[0])
        try:
            if ruta == "/api/index":
                return self.responder(200, indice_examenes())
            if ruta == "/api/temas":
                return self.responder(200, {"temas": temas()})
            if ruta.startswith("/api/tema/"):
                return self.responder(200, leer_tema(ruta[len("/api/tema/"):]))
        except Exception as e:
            return self.responder(400, {"error": str(e)})
        return super().do_GET()

    def do_POST(self):
        ruta = urllib.parse.unquote(self.path.split("?")[0])
        try:
            largo = int(self.headers["Content-Length"])
            if largo > LIMITE_CUERPO:
                return self.responder(400, {"error": "cuerpo demasiado grande"})
            crudo = self.rfile.read(largo)
            if ruta == "/api/voz":
                return self.responder(200, transcribir(crudo))
            if ruta == "/api/intento":
                datos = json.loads(crudo)
                return self.responder(200, {"ruta": guardar_intento(datos["slug"], datos["examen"], datos["respuestas"])})
            if not ruta.startswith("/api/tema/"):
                return self.responder(404, {"error": "no existe"})
            self.responder(200, guardar_tema(ruta[len("/api/tema/"):], json.loads(crudo)))
        except Exception as e:
            self.responder(400, {"error": str(e)})

    def end_headers(self):
        if self.path.endswith((".html", ".css", ".js")):
            self.send_header("Cache-Control", "no-store")   # editar y recargar, sin F5 duro
        super().end_headers()

    def log_message(self, *a):
        pass  # ponytail: sin ruido en consola; sacar el pass para debug


if __name__ == "__main__":
    if sys.argv[1:2] == ["--transcribir"]:
        print(" ".join(t for _, t in whisper(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "es")).strip())
        sys.exit(0)
    pagina = sys.argv[1] if len(sys.argv) > 1 else ""
    url = f"http://localhost:{PUERTO}/{pagina}"
    try:
        servidor = http.server.ThreadingHTTPServer(("127.0.0.1", PUERTO), Handler)
    except OSError:
        # ponytail: ya hay un server levantado, abrimos la pagina y listo
        print(f"Ya habia un servidor en {PUERTO}. Abriendo {url}")
        webbrowser.open(url)
        sys.exit(0)
    print(f"Estudios en {url}  (ctrl+c para cortar)")
    webbrowser.open(url)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor apagado.")  # ctrl+c sin traceback
