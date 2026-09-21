#!/usr/bin/env python3
"""Autocomprobacion de guardar_intento() (POST /api/intento): python3 app/test_intento.py"""
import base64, json, pathlib, shutil, sys, tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import server


def con_tema_de_prueba(f):
    def envuelto():
        tmp = pathlib.Path(tempfile.mkdtemp()).resolve()   # mismo simlink-resuelto que usa carpeta()
        raiz_real, temas_real = server.RAIZ, server.TEMAS
        server.RAIZ, server.TEMAS = tmp, tmp / "temas"
        d = server.TEMAS / "demo" / "examenes" / "cap-01"
        d.mkdir(parents=True)
        (d / "examen.json").write_text('{"titulo": "demo", "preguntas": []}')
        try:
            f()
        finally:
            server.RAIZ, server.TEMAS = raiz_real, temas_real
            shutil.rmtree(tmp)
    return envuelto


def espera_rechazo(f):
    try:
        f()
    except ValueError:
        return
    raise AssertionError("debio rechazar: " + f.__name__)


@con_tema_de_prueba
def test_escribe_intento():
    ruta = server.guardar_intento("demo", "cap-01", [{"i": 0, "tipo": "opcion_multiple", "elegida": 1}])
    archivo = server.RAIZ / ruta
    assert archivo.is_file(), "no escribio el archivo"
    datos = json.loads(archivo.read_text())
    assert datos == {"examen": "cap-01", "respuestas": [{"i": 0, "tipo": "opcion_multiple", "elegida": 1}]}


@con_tema_de_prueba
def test_guarda_audio_oral():
    crudo = b"\x00\x01audio-falso"
    ruta = server.guardar_intento("demo", "cap-01", [
        {"i": 2, "tipo": "oral", "audio": base64.b64encode(crudo).decode(), "mime": "audio/webm;codecs=opus"}])
    datos = json.loads((server.RAIZ / ruta).read_text())
    nombre = datos["respuestas"][0]["audio"]
    assert nombre == ruta.split("/")[-1].replace(".json", "-p2.webm")
    assert (server.RAIZ / ruta).parent.joinpath(nombre).read_bytes() == crudo
    assert "mime" not in datos["respuestas"][0], "no debe quedar el mime en el json"


@con_tema_de_prueba
def test_rechaza_slug_inexistente():
    espera_rechazo(lambda: server.guardar_intento("../fuera", "cap-01", []))


@con_tema_de_prueba
def test_rechaza_examen_que_escapa():
    espera_rechazo(lambda: server.guardar_intento("demo", "../../fuera", []))


@con_tema_de_prueba
def test_rechaza_examen_inexistente():
    espera_rechazo(lambda: server.guardar_intento("demo", "no-existe", []))


if __name__ == "__main__":
    test_escribe_intento()
    test_guarda_audio_oral()
    test_rechaza_slug_inexistente()
    test_rechaza_examen_que_escapa()
    test_rechaza_examen_inexistente()
    print("ok")
