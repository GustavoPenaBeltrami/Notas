<a id="readme-top"></a>

[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

<br />
<div align="center">
<h3 align="center">Notas</h3>

  <p align="center">
    Un ecosistema de estudio para cualquier cosa que quieras aprender: skills y agentes que enseñan, examinan y corrigen, un filesystem de temas en Markdown y una app local para tomar notas y rendir.
    <br />
    <a href="docs/manual.md"><strong>Ver el manual »</strong></a>
    <br />
    <br />
    <a href="https://github.com/GustavoPenaBeltrami/Notas/issues/new?labels=bug">Reportar un bug</a>
    &middot;
    <a href="https://github.com/GustavoPenaBeltrami/Notas/issues/new?labels=enhancement">Pedir una feature</a>
  </p>
</div>

<details>
  <summary>Contenido</summary>
  <ol>
    <li><a href="#el-proyecto">El proyecto</a>
      <ul><li><a href="#hecho-con">Hecho con</a></li></ul>
    </li>
    <li><a href="#empezar">Empezar</a>
      <ul>
        <li><a href="#requisitos">Requisitos</a></li>
        <li><a href="#instalación">Instalación</a></li>
      </ul>
    </li>
    <li><a href="#uso">Uso</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contribuir">Contribuir</a></li>
    <li><a href="#contacto">Contacto</a></li>
    <li><a href="#agradecimientos">Agradecimientos</a></li>
  </ol>
</details>

## El proyecto

Un libro, una certificación, la documentación de una herramienta, un curso:
cada cosa que estudiás es un **tema**, y Notas le arma alrededor el loop
completo — preparación, práctica, feedback, repaso espaciado.

Son cuatro piezas que se hablan a través del filesystem:

- **Skills** (`agente/skills/`) — el método. Enseñar desde verdades
  incondicionales, armar exámenes y ejercicios, corregir contra una rúbrica,
  repasar con tarjetas Leitner.
- **Agentes** (`agente/agents/`) — un `investigador` que verifica antes de
  afirmar, y un `profesor-<tema>` con la persona justa para cada tema.
- **Filesystem** (`temas/<tema>/`) — notas en Markdown de verdad, exámenes en
  JSON, intentos, correcciones, progreso. Legible en GitHub, Obsidian o
  cualquier editor. Sin base de datos.
- **App** (`app/`) — un cuaderno y un simulador de examen en el navegador,
  servidos en local. Dictado por voz con Whisper, diagramas Mermaid y
  fórmulas LaTeX.

No depende de un agente en particular: las skills están en formato
`SKILL.md` y `AGENTS.md` le explica el proyecto a cualquiera — Claude Code,
Codex, Gemini CLI, Antigravity, Cline, Cursor, opencode, con un modelo en la
nube o local vía Ollama.

<p align="right">(<a href="#readme-top">volver arriba</a>)</p>

### Hecho con

* [![Python][Python-shield]][Python-url] — sólo la stdlib
* [![JavaScript][JS-shield]][JS-url] — sin frameworks ni build
* [![Mermaid][Mermaid-shield]][Mermaid-url] y [![KaTeX][KaTeX-shield]][KaTeX-url]
* [mlx-whisper](https://github.com/ml-explore/mlx-examples) — dictado local, opcional

<p align="right">(<a href="#readme-top">volver arriba</a>)</p>

## Empezar

### Requisitos

* Python 3 y npm (sólo como atajo para `npm run app`; no hay `npm install`)
* [uv](https://docs.astral.sh/uv/) para el dictado — baja mlx-whisper solo la primera vez (Apple Silicon)
* Un agente de código, el que uses

### Instalación

1. Cloná el repo
   ```sh
   git clone https://github.com/GustavoPenaBeltrami/Notas.git
   cd Notas
   ```
2. Abrí tu agente en la carpeta y pedile:
   ```
   Leé AGENTS.md y corré notas-setup-agente.
   ```
   Detecta qué agente es y expone las skills en su formato — symlinks si las
   soporta, conversión si no. Lo que crea queda en `.git/info/exclude`, así
   que no ensucia el repo.
3. Levantá la app
   ```sh
   npm run app
   ```
4. Cambiá el remote si vas a guardar tus temas en un repo propio
   ```sh
   git remote set-url origin <tu-repo>
   ```

<p align="right">(<a href="#readme-top">volver arriba</a>)</p>

## Uso

Se usa con **tres ventanas** lado a lado:

| | Ventana | Para qué |
|---|---|---|
| 1 | **El material** | El PDF, el curso, la documentación. Lo que estás estudiando. |
| 2 | **La app** (`npm run app`) | El cuaderno en `localhost:8321`. Los exámenes, desde la barra de navegación. |
| 3 | **El agente** | Abierto en la raíz del repo. Enseña, arma exámenes, corrige. |

Todo arranca en la ventana 3:

```
/notas-init      dar de alta un tema: entrevista, estructura, diagnóstico de nivel
/notas-sesion    qué hay pendiente hoy en todos los temas, y qué hacer
```

Después el loop: `/notas-ensenar` o `/notas-resumir` para preparar,
`/notas-examen` y `/notas-ejercicios` para practicar (rendís en la ventana 2),
`/notas-correjir` para el feedback y `/notas-repasar` para que no se evapore.
Todo lo que producen queda en `temas/<tema>/` y aparece solo en la app.

`temas/ejemplo/` muestra la estructura. Tus temas reales quedan fuera de git.

_Detalle de cada skill, del cuaderno y del formato de examen en el [manual](docs/manual.md)._

<p align="right">(<a href="#readme-top">volver arriba</a>)</p>

## Roadmap

- [x] Cuaderno con dictado, diagramas y fórmulas
- [x] Examen con opción múltiple, desarrollo, oral y práctico
- [x] Skills y agentes independientes del agente
- [ ] Probar `notas-setup-agente` en Codex, Gemini CLI, Antigravity y Cline
- [ ] Dictado fuera de Apple Silicon

Ver los [issues abiertos](https://github.com/GustavoPenaBeltrami/Notas/issues).

<p align="right">(<a href="#readme-top">volver arriba</a>)</p>

## Contribuir

1. Hacé un fork
2. Creá tu rama (`git checkout -b feature/algo`)
3. Commiteá (`git commit -m 'Agrega algo'`)
4. Pusheá (`git push origin feature/algo`)
5. Abrí un Pull Request

Las skills se editan en `agente/skills/`, nunca en la carpeta de un agente.

<p align="right">(<a href="#readme-top">volver arriba</a>)</p>

## Contacto

Gustavo Peña Beltrami — [github.com/GustavoPenaBeltrami/Notas](https://github.com/GustavoPenaBeltrami/Notas)

<p align="right">(<a href="#readme-top">volver arriba</a>)</p>

## Agradecimientos

* [amosblomqvist/learn](https://github.com/amosblomqvist/learn) — el método de `notas-ensenar`
* [Matt Pocock](https://github.com/mattpocock) — la memoria por tema y el repaso espaciado
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#readme-top">volver arriba</a>)</p>

[stars-shield]: https://img.shields.io/github/stars/GustavoPenaBeltrami/Notas.svg?style=for-the-badge
[stars-url]: https://github.com/GustavoPenaBeltrami/Notas/stargazers
[issues-shield]: https://img.shields.io/github/issues/GustavoPenaBeltrami/Notas.svg?style=for-the-badge
[issues-url]: https://github.com/GustavoPenaBeltrami/Notas/issues
[Python-shield]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[JS-shield]: https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black
[JS-url]: https://developer.mozilla.org/docs/Web/JavaScript
[Mermaid-shield]: https://img.shields.io/badge/Mermaid-FF3670?style=for-the-badge&logo=mermaid&logoColor=white
[Mermaid-url]: https://mermaid.js.org/
[KaTeX-shield]: https://img.shields.io/badge/KaTeX-329894?style=for-the-badge
[KaTeX-url]: https://katex.org/
