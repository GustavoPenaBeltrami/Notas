"""Conversion HTML <-> Markdown para el subconjunto que usa el editor.

Bloques:  h1-h6, p, ul/li, y HTML crudo en su propia linea (tarjetas, figuras).
Inline:   strong/b -> **, em/i -> *, s/del -> ~~, a.ref -> [[x]].
Crudo:    mark, u, span, aside, figure, img se guardan como HTML dentro del .md.
          Markdown acepta HTML inline, asi que el archivo sigue abriendose bien
          en Obsidian y conserva colores, comentarios y posiciones.

Autocomprobacion: python3 app/texto.py
"""
import re
import unicodedata
from html import escape as _escape, unescape as _unescape
from html.parser import HTMLParser

CRUDO = {"mark", "u", "span", "aside", "figure", "figcaption", "img", "br"}
VACIOS = {"br", "img", "hr"}
INLINE = {"strong": "**", "b": "**", "em": "*", "i": "*",
          "s": "~~", "del": "~~", "strike": "~~"}
BLOQUE = {"p", "div", "li", "ul", "ol", "h1", "h2", "h3", "h4", "h5", "h6"}

VIZ = {"mermaid", "math"}
_FIGURA = re.compile(r"<figure\b([^>]*)>\s*<pre\b[^>]*>(.*?)</pre>.*?</figure>", re.S)
_KIND = re.compile(r'data-kind="([a-z]+)"')
_APERTURA = re.compile(r"^```([a-z]+)\s*$")


def _figura(kind, fuente):
    """Bloque atomico: el <pre> es la fuente, el <div> lo pinta viz.js."""
    return (f'<figure class="viz" data-kind="{kind}" contenteditable="false">'
            f'<pre class="src">{_escape(fuente, quote=False)}</pre>'
            f'<div class="view"></div></figure>')


def slug(texto, defecto="seccion"):
    t = unicodedata.normalize("NFD", texto)
    t = "".join(c for c in t if unicodedata.category(c) != "Mn").lower()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", t)).strip("-") or defecto


def _abrir(tag, attrs):
    return "<" + tag + "".join(f' {k}="{v}"' for k, v in attrs if v is not None) + ">"


class _AMarkdown(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.partes = []
        self.crudo = 0      # profundidad dentro de un elemento que se copia tal cual
        self.ref = None     # texto acumulado de un <a class="ref">
        self.enbloque = 0   # dentro de un p/h/li: una imagen ahi va inline
        self.listas = []

    def handle_starttag(self, tag, attrs):
        if self.crudo:
            self.partes.append(_abrir(tag, attrs))
            if tag not in VACIOS:
                self.crudo += 1
            return
        if tag in CRUDO:
            if tag in ("aside", "figure") or (tag == "img" and not self.enbloque):
                self.partes.append("\n\n")      # bloque propio, renglon propio
            self.partes.append(_abrir(tag, attrs))
            if tag not in VACIOS:
                self.crudo = 1
            return
        clases = dict(attrs).get("class", "")
        if tag == "a" and "ref" in clases:
            self.ref = ""
            return
        if tag in INLINE:
            self.partes.append(INLINE[tag])
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.enbloque += 1
            self.partes.append("\n\n" + "#" * int(tag[1]) + " ")
        elif tag in ("ul", "ol"):
            self.listas.append([tag, 0])
        elif tag == "li":
            self.enbloque += 1
            if self.listas and self.listas[-1][0] == "ol":
                self.listas[-1][1] += 1
                self.partes.append(f"\n{self.listas[-1][1]}. ")
            else:
                self.partes.append("\n- ")
        elif tag in ("p", "div"):
            self.enbloque += 1
            self.partes.append("\n\n")

    def handle_startendtag(self, tag, attrs):
        self.partes.append(_abrir(tag, attrs)) if (self.crudo or tag in CRUDO) \
            else self.partes.append("\n" if tag == "br" else "")

    def handle_endtag(self, tag):
        if self.crudo:
            self.partes.append(f"</{tag}>")
            self.crudo -= 1
            if self.crudo == 0 and tag in ("aside", "figure"):
                self.partes.append("\n\n")
            return
        if tag == "a" and self.ref is not None:
            self.partes.append(f"[[{self.ref.strip()}]]")
            self.ref = None
        elif tag in INLINE:
            self.partes.append(INLINE[tag])
        elif tag == "li":
            self.enbloque = max(0, self.enbloque - 1)   # el proximo <li> abre su renglon
        elif tag in ("ul", "ol"):
            if self.listas:
                self.listas.pop()
            self.partes.append("\n\n")
        elif tag in BLOQUE:
            self.enbloque = max(0, self.enbloque - 1)
            self.partes.append("\n")

    def handle_data(self, datos):
        if self.crudo:
            self.partes.append(datos)
        elif self.ref is not None:
            self.ref += datos
        elif datos.strip() == "" and "\n" in datos:
            pass          # salto entre bloques de nuestro propio HTML, no texto
        else:
            self.partes.append(datos.replace("\n", " "))


def html_a_md(html):
    # Los dibujos salen del parser: vuelven como fence al final, con su fuente
    # intacta. Lo que haya pintado el navegador adentro de la figura se tira.
    guardados = []

    def _apartar(m):
        atributos, fuente = m.group(1), m.group(2)
        if 'class="viz"' not in atributos:
            return m.group(0)
        k = _KIND.search(atributos)
        kind = k.group(1) if k and k.group(1) in VIZ else "mermaid"
        guardados.append((kind, _unescape(fuente)))
        return f"<p>@@VIZ{len(guardados) - 1}@@</p>"

    html = _FIGURA.sub(_apartar, html)
    # Un bloque vacio es un renglon en blanco que el usuario puso a proposito.
    # Markdown no tiene forma de representarlo, asi que queda como <br> crudo.
    html = re.sub(r"<(p|div)\b[^>]*>(?:\s|<br\s*/?>|&nbsp;)*</\1>", "<br>", html)
    p = _AMarkdown()
    p.feed(html)
    p.close()
    md = "".join(p.partes)
    md = re.sub(r"@@VIZ(\d+)@@",
                lambda m: "\n\n```{0}\n{1}\n```\n\n".format(*guardados[int(m.group(1))]), md)
    md = re.sub(r"[ \t]+\n", "\n", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip() + "\n"


def _inline(linea):
    linea = re.sub(r"\[\[([^\]]+)\]\]",
                   lambda m: f'<a class="ref" href="#{slug(m.group(1))}">{m.group(1)}</a>', linea)
    linea = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", linea)
    linea = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<i>\1</i>", linea)
    linea = re.sub(r"~~(.+?)~~", r"<s>\1</s>", linea)
    return linea


def md_a_html(md):
    salida, lista = [], None
    lineas = md.split("\n")
    i = 0

    def cerrar():
        nonlocal lista
        if lista:
            salida.append(f"</{lista}>")
            lista = None

    def item(tipo, texto):
        nonlocal lista
        if lista != tipo:
            cerrar()
            salida.append(f"<{tipo}>")
            lista = tipo
        salida.append(f"<li>{_inline(texto)}</li>")

    while i < len(lineas):
        cruda = lineas[i].rstrip()
        i += 1
        abre = _APERTURA.match(cruda.strip())
        if abre and abre.group(1) in VIZ:
            cerrar()
            cuerpo = []
            while i < len(lineas) and lineas[i].strip() != "```":
                cuerpo.append(lineas[i])
                i += 1
            i += 1
            salida.append(_figura(abre.group(1), "\n".join(cuerpo).strip("\n")))
            continue
        if not cruda.strip():
            cerrar()
            continue
        if cruda.lstrip().startswith("<"):          # tarjeta o figura: tal cual
            cerrar()
            # un <br> solo es un renglon en blanco: parrafo vacio, no <br> suelto
            # (suelto colapsa contra los margenes vecinos y el hueco sale disparejo)
            salida.append("<p><br></p>" if cruda.strip() in ("<br>", "<br/>", "<br />") else cruda)
            continue
        enc = re.match(r"(#{1,6}) (.*)", cruda)
        num = re.match(r"\d+\. (.*)", cruda)
        if enc:
            cerrar()
            n = len(enc.group(1))
            salida.append(f"<h{n}>{_inline(enc.group(2))}</h{n}>")
        elif cruda.startswith("- "):
            item("ul", cruda[2:])
        elif num:
            item("ol", num.group(1))
        else:
            cerrar()
            salida.append(f"<p>{_inline(cruda)}</p>")
    cerrar()
    return "\n".join(salida)


def partir_por_h1(html):
    """[(titulo, html)] por cada h1. Lo que venga antes del primer h1 va aparte."""
    trozos = re.split(r"(?=<h1[ >])", html)
    secciones = []
    for t in trozos:
        if not t.strip():
            continue
        m = re.match(r"<h1[^>]*>(.*?)</h1>", t, re.S)
        titulo = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else "Sin titulo"
        secciones.append((titulo, t))
    return secciones


if __name__ == "__main__":
    h = ('<h1>Fundamentos</h1><p>Texto con <b>negrita</b> y <i>cursiva</i> y <s>tachado</s>.</p>'
         '<h2>Acoplamiento</h2><ul><li>Uno</li><li>Dos</li></ul>'
         '<p>Ver <a class="ref" href="#estilos">Estilos</a> tambien.</p>'
         '<p>Un <mark class="mk mk-fondo" style="--c: #D9C46A" title="ojo">resaltado</mark> vivo.</p>')
    md = html_a_md(h)
    assert "# Fundamentos" in md, md
    assert "## Acoplamiento" in md, md
    assert "**negrita**" in md and "*cursiva*" in md and "~~tachado~~" in md, md
    assert "- Uno\n- Dos" in md, md
    assert "[[Estilos]]" in md, md
    assert '<mark class="mk mk-fondo" style="--c: #D9C46A" title="ojo">resaltado</mark>' in md, md

    ida = md_a_html(md)
    assert "<h1>Fundamentos</h1>" in ida, ida
    assert "<b>negrita</b>" in ida and "<i>cursiva</i>" in ida, ida
    assert "<li>Uno</li>" in ida and "<ul>" in ida, ida
    assert '<a class="ref" href="#estilos">Estilos</a>' in ida, ida
    assert "<mark" in ida and 'title="ojo"' in ida, ida

    # ida y vuelta estable: convertir dos veces no cambia nada
    assert html_a_md(ida) == md, html_a_md(ida) + "\n---\n" + md

    secciones = partir_por_h1(ida)
    assert len(secciones) == 1 and secciones[0][0] == "Fundamentos", secciones

    # un renglon en blanco es intencional: sobrevive como <br> crudo
    for entrada in ('<p>uno</p><p><br></p><p>dos</p>',
                    '<h2>T</h2><div><br></div><p>x</p>',
                    '<p>a</p><div></div><p>b</p>',
                    '<p>uno<br>dos</p>'):
        md1 = html_a_md(entrada)
        assert "<br>" in md1, (entrada, md1)
        assert html_a_md(md_a_html(md1)) == md1, (md1, html_a_md(md_a_html(md1)))

    # dibujos: el fence es la fuente de verdad y sobrevive la ida y vuelta
    md_viz = ("# Cap\n\ntexto\n\n```mermaid\ngraph TD\n  A[Paquete] --> B{Orden}\n"
              "```\n\nmas texto\n\n```math\np_{99} = \\frac{x}{y}\n```\n")
    h_viz = md_a_html(md_viz)
    assert '<figure class="viz" data-kind="mermaid"' in h_viz, h_viz
    assert "A[Paquete] --&gt; B{Orden}" in h_viz, h_viz
    assert '<figure class="viz" data-kind="math"' in h_viz, h_viz
    assert html_a_md(h_viz) == md_viz, html_a_md(h_viz)

    # lo que el navegador pinte adentro de la figura se descarta al guardar
    pintado = h_viz.replace('<div class="view"></div>',
                            '<div class="view"><svg><g>basura</g></svg></div>', 1)
    assert html_a_md(pintado) == md_viz, html_a_md(pintado)

    # una figura que no es un dibujo sigue copiandose tal cual
    otra = '<figure><img src="x.png"><figcaption>pie</figcaption></figure>'
    assert "<figcaption>pie</figcaption>" in html_a_md(otra), html_a_md(otra)

    # un fence pegado a una lista corta la lista, no se la come
    md_lista = "- uno\n- dos\n\n```mermaid\ngraph LR\n  A --> B\n```\n"
    assert md_a_html(md_lista).count("</ul>") == 1, md_a_html(md_lista)
    assert html_a_md(md_a_html(md_lista)) == md_lista, html_a_md(md_a_html(md_lista))

    md_num = "1. uno\n2. dos\n\n- a\n- b\n"
    h_num = md_a_html(md_num)
    assert "<ol>" in h_num and "<ul>" in h_num, h_num
    assert html_a_md(h_num) == md_num, html_a_md(h_num)

    dos = partir_por_h1("<h1>Uno</h1><p>a</p><h1>Dos</h1><p>b</p>")
    assert [t for t, _ in dos] == ["Uno", "Dos"], dos
    assert slug("Cap 1 — Introducción") == "cap-1-introduccion"
    print("texto.py ok")
