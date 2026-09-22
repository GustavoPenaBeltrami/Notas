<div align="center">

<!-- omit in toc -->

# Notas 📚

<strong>Hub para autodidactas agentizado</strong>

*Hecho por [Gustavo Peña Beltrami](https://github.com/GustavoPenaBeltrami)*

[![Manual](https://img.shields.io/badge/docs-manual-blue)](docs/manual.md)
[![Stars](https://img.shields.io/github/stars/GustavoPenaBeltrami/Notas.svg)](https://github.com/GustavoPenaBeltrami/Notas/stargazers)
[![Issues](https://img.shields.io/github/issues/GustavoPenaBeltrami/Notas.svg)](https://github.com/GustavoPenaBeltrami/Notas/issues)
[![Python](https://img.shields.io/badge/python-server-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Local](https://img.shields.io/badge/local-development-2EA44F?logo=homeassistant&logoColor=white)](#instalación)

</div>

---

Un libro, una certificación, la documentación de una herramienta, un curso: cada cosa que estudiás es un **tema**, y Notas le arma alrededor el loop completo — preparación, práctica, feedback, repaso espaciado. Todo arranca con una línea en tu agente:

```
/notas-init      dar de alta un tema: entrevista, estructura, diagnóstico de nivel
/notas-sesion    qué hay pendiente hoy en todos los temas, y qué hacer
```

## Por qué Notas

Estudiar bien es más difícil de lo que parece. Leer no alcanza: hace falta que alguien te explique, te tome examen, te corrija y te haga repasar justo antes de olvidarte. Notas se encarga de todo eso. Vos estudiás el material, el agente enseña y corrige, y todo queda en Markdown en tu disco: **con Notas, el método ya viene incluido.**

**No depende de un agente en particular.** Las skills están en formato `SKILL.md` y `AGENTS.md` le explica el proyecto a cualquiera — Claude Code, Codex, Gemini CLI, Antigravity, Cline, Cursor, opencode, con un modelo en la nube o local vía Ollama.

Notas tiene cuatro piezas que se hablan a través del filesystem:

<table>
<tr>
<td align="center" valign="top" width="25%">
<strong>🧠 Skills</strong>
<br /><code>agente/skills/</code>
<br />Enseñar, armar exámenes y ejercicios, corregir con rúbrica, repasar con Leitner.
</td>
<td align="center" valign="top" width="25%">
<strong>🎓 Agentes</strong>
<br /><code>agente/agents/</code>
<br />Un <code>investigador</code> que verifica antes de afirmar y un <code>profesor-&lt;tema&gt;</code> por tema.
</td>
<td align="center" valign="top" width="25%">
<strong>🗂️ Filesystem</strong>
<br /><code>temas/&lt;tema&gt;/</code>
<br />Notas en Markdown, exámenes en JSON, intentos, correcciones y progreso. Sin base de datos.
</td>
<td align="center" valign="top" width="25%">
<strong>📓 App</strong>
<br /><code>app/</code>
<br />Cuaderno y simulador de examen en local, con dictado, Mermaid y LaTeX.
</td>
</tr>
</table>

Las **skills** son el método: enseñar desde verdades incondicionales, practicar y repasar. Los **agentes** le ponen la persona justa a cada tema. El **filesystem** se lee en GitHub, Obsidian o cualquier editor. Y la **app** es donde tomás notas y rendís, con dictado por voz vía Whisper.

¿Listo para empezar? Seguí la [instalación](#instalación) o saltá directo al [manual](docs/manual.md).

## Tres ventanas

Notas se usa con tres ventanas lado a lado:

| | Ventana | Para qué |
|---|---|---|
| 1 | **El material** | El PDF, el curso, la documentación. Lo que estás estudiando. |
| 2 | **La app** (`npm run app`) | El cuaderno en `localhost:8321`. Los exámenes, desde la barra de navegación. |
| 3 | **El agente** | Abierto en la raíz del repo. Enseña, arma exámenes, corrige. |

Después el loop: `/notas-ensenar` o `/notas-resumir` para preparar, `/notas-examen` y `/notas-ejercicios` para practicar (rendís en la ventana 2), `/notas-correjir` para el feedback y `/notas-repasar` para que no se evapore. Todo lo que producen queda en `temas/<tema>/` y aparece solo en la app.

`temas/ejemplo/` muestra la estructura. Tus temas reales quedan fuera de git.

## Instalación

Corre en macOS, Linux y Windows. Necesitás:

- **Python 3.9+**
- **[uv](https://docs.astral.sh/uv/)** — trae el motor de dictado la primera vez: mlx-whisper en Mac Apple Silicon, faster-whisper en el resto
- **Un agente de código**, el que uses
- npm es opcional: `npm run app` es sólo un atajo, no hay `npm install`

Sin uv, `python3 app/server.py app/notas.html` levanta todo menos el dictado. En Windows ARM, el dictado corre con Python x64 emulado (ver el [manual](docs/manual.md#arrancar)).

```sh
git clone https://github.com/GustavoPenaBeltrami/Notas.git
cd Notas
```

Abrí tu agente en la carpeta y pedile:

```
Leé AGENTS.md y corré notas-setup-agente.
```

Detecta qué agente es y expone las skills en su formato — symlinks si las soporta, conversión si no. Lo que crea queda en `.git/info/exclude`, así que no ensucia el repo. Después levantá la app:

```sh
npm run app
```

**¿Vas a guardar tus temas en un repo propio?** Cambiá el remote:

```sh
git remote set-url origin <tu-repo>
```

## 📚 Documentación

El detalle de cada skill, del cuaderno y del formato de examen está en el **[manual](docs/manual.md)**.

**Roadmap:** probar `notas-setup-agente` en Codex, Gemini CLI, Antigravity y Cline, y dictado nativo en Windows ARM. Ver los [issues abiertos](https://github.com/GustavoPenaBeltrami/Notas/issues).

**Gracias a** [amosblomqvist/learn](https://github.com/amosblomqvist/learn) por el método de `notas-ensenar` y a [Matt Pocock](https://github.com/mattpocock) por la memoria por tema y el repaso espaciado.

## Contribuir

¡Las contribuciones son bienvenidas! Hacé un fork, creá tu rama, y abrí un Pull Request. Las skills se editan en `agente/skills/`, nunca en la carpeta de un agente. Para bugs o ideas, [abrí un issue](https://github.com/GustavoPenaBeltrami/Notas/issues/new).
