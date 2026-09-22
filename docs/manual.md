# Manual

Referencia completa. La presentación está en el [README](../README.md).

## Arrancar

```sh
npm run app      # abre los cuadernos; los examenes desde la nav
```

Levanta el servidor en `http://localhost:8321/` y abre `notas.html`. Si ya hay
uno corriendo, abre la pestana y sale. Sin `npm install` y sin build: corre sobre la stdlib de Python.
La única excepción es el dictado: `npm run app` arranca con `uv run`, que lee
las dependencias del encabezado de `app/server.py` y baja la que corresponde la
primera vez — `mlx-whisper` (GPU) en Mac Apple Silicon, `faster-whisper` (CPU)
en Linux, Windows y Mac Intel. En CPU usa el modelo `small`; para otro,
`NOTAS_MODELO_VOZ=turbo npm run app`. En Windows ARM el dictado necesita Python
x64 (emulado): `uv run --python cpython-3.12-windows-x86_64-none --with faster-whisper app/server.py app/notas.html`.
Sin `uv`, `python3 app/server.py app/notas.html` levanta todo menos el dictado.

## Archivos

```
README.md            La presentación.
package.json         `npm run app`. Sin dependencias.
AGENTS.md            Entrada para cualquier agente: dónde están las skills y cómo traducir herramientas.
agente/
    skills/          Las skills de abajo. Fuente única, para cualquier agente.
    agents/          investigador (verifica antes de enseñar) y un profesor-<tema> por tema (personales, ignorados).
docs/manual.md       Esto.
app/
    server.py        Servidor local. Lista archivos, arma y guarda los cuadernos.
    texto.py         Conversión HTML <-> Markdown. `python3 app/texto.py` se autotestea.
    estilo.css       Sistema visual compartido. Tokens y temas.
    tema.js          Lista de temas y selector, compartido.
    shell.js         Waybar, explorer y statusline, compartidos.
    examen.html      Simulador de examen. Rinde los 4 tipos de pregunta.
    notas.html       Cuaderno de notas.
    viz.js           Diagramas (Mermaid) y fórmulas (KaTeX). Compartido.
    Design.md        El sistema visual: tokens, componentes, do's y don'ts.
temas/<tema>/
    tema.json          Título, subtítulo, tipo, área, objetivos, motivo, idioma, rutina, enlaces.
    aprendizaje.md     Misión, glosario y registro. La memoria de /notas-ensenar.
    notas/NN-*.md      Una sección por archivo. Markdown de verdad.
    notas/img/         Las imágenes pegadas, como archivos sueltos.
    recursos/          PDFs, apuntes, lo que quieras tener a mano.
    examenes/<slug>/
        examen.json    Preguntas: opción múltiple, desarrollo, oral o práctico.
        intentos/      Un .json (respuestas) y un .md (corrección) por intento rendido.
    ejercicios/<slug>/
        enunciado.md   Consigna aplicada: producir un artefacto, no responder.
        intentos/      El artefacto entregado y su .md de corrección.
    progreso/
        status.md      Dónde estoy hoy en este tema.
        log.md          Historial: lectura, exámenes, ejercicios, repasos.
temas/repaso/         Lo crea /notas-repasar. Un examen fechado por repaso.
```

Los frontends leen el filesystem: cualquier `<slug>/examen.json` que pongas en
`examenes/` aparece solo en la lista, y las secciones del cuaderno salen de
los `.md`. No hay índice que mantener a mano.

## El sistema visual

`app/Design.md` es la fuente. La app imita un escritorio tiling en una pestaña:
waybar arriba (navegación y herramientas), explorer a la izquierda con todos los
temas y sus índices, el contenido como un buffer de vim en el medio (números de
línea, `~` al final) y una statusline abajo (modo, ruta, guardado, zoom, ancho).
JetBrains Mono en todo, superficies planas, sin sombras. Los títulos se
distinguen por color ANSI, no por tamaño.

Hay seis temas en el selector de la waybar: `hypr` (navy, el default oscuro),
`claro`, `e-ink` (monocromo oscuro), `sakura`, `bosque` y `ámbar crt`. Cada uno
es un bloque de 20 tokens en `estilo.css`. Para sumar uno, se copia un bloque y
se agrega la clave en `TEMAS` de `tema.js`. Los componentes sólo leen tokens:
tocá ahí, no en las reglas sueltas.

El selector de fuente de lectura del cuaderno (mono / serif / inter) aplica sólo
al cuerpo de la nota.

## Diagramas y fórmulas

En el cuaderno, los botones ⌗ y Σ insertan un bloque de diagrama (Mermaid) o de
fórmula (LaTeX). Se hace clic encima para editar la fuente y se redibuja solo.

El bloque es atómico: no se escribe adentro. Lo que manda es su texto fuente; el
dibujo se descarta al guardar, así que en el `.md` queda un fence limpio:

    ```mermaid
    graph TD
      A[Paquete] --> B[Stream confiable]
    ```

Eso significa que el archivo también renderiza en GitHub y en Obsidian, y que se
puede escribir el fence a mano en el `.md` sin abrir la app. `examen.html`
renderiza los mismos fences dentro del enunciado, las opciones y la explicación.

Mermaid y KaTeX se bajan de CDN la primera vez, así que sin internet los bloques
muestran su fuente en vez del dibujo. Matemática en medio de un renglón no está
soportada: sólo bloques.

## Cómo se usa

La puerta de entrada es `/notas-sesion`: releva el estado de todos los temas
(repasos vencidos, intentos sin corregir, temas sin ejercicios) y pregunta qué
querés hacer. Para un tema nuevo, `/notas-init` entrevista, crea el filesystem
de arriba y hace un diagnóstico de nivel.

Adentro de un tema, el loop es preparación → práctica → feedback → iteración:

1. **Preparación** — leo con `recursos/` y `enlaces` de `tema.json`, tomo
   notas en **notas.html**, o `/notas-resumir` condensa un texto que ya
   entiendo. Cuando algo no entra leyéndolo, `/notas-ensenar` lo construye
   desde cero (ver abajo).
2. **Práctica** — `/notas-examen` arma un examen (`examenes/<slug>/`) para
   responder sobre el tema; `/notas-ejercicios` arma un ejercicio
   (`ejercicios/<slug>/`) para producir algo con el tema — código, un ADR,
   una crítica. Rindo el examen en **examen.html**.
3. **Feedback** — `/notas-correjir` corrige el intento, examen o ejercicio,
   contra la rúbrica o la consigna, y actualiza `aprendizaje.md` y `progreso/`.
4. **Iteración** — `/notas-repasar` arma un repaso espaciado e intercalado
   (tarjetas Leitner) para que lo entendido no se evapore.

## Temas

Un **tema** es cualquier fuente de estudio, no sólo un libro. El campo `tipo`
de `tema.json` dice cuál es: `libro`, `certificación`, `documentación`, `curso`
o `práctica`. El tipo cambia dos cosas: la etiqueta que ves en las listas y
cómo `notas-examen` escribe las preguntas (un examen de certificación imita el
formato real del examen, uno de documentación pregunta cuándo usar qué).

```json
{
  "titulo": "AWS Certified Cloud Practitioner",
  "subtitulo": "CLF-C02 · 65 preguntas en 90 min · aprueba con 700 de 1000",
  "tipo": "certificación",
  "area": "cloud",
  "orden": 3,
  "objetivos": ["Poder elegir el servicio correcto por trade-offs, no por nombre conocido."],
  "motivo": "Necesito la certificación para el rol.",
  "idioma": { "fuente": "en", "notas": "es", "examenes": "es" },
  "rutina": { "cadencia": "1 dominio por semana", "sesion": "~30 min" },
  "fecha_fin": "YYYY-MM-DD",
  "enlaces": [
    { "titulo": "Guía del examen", "url": "https://docs.aws.amazon.com/..." }
  ]
}
```

`area` agrupa temas afines (por ejemplo varios libros de arquitectura de
software) como dato de contexto/tono. El agente-profesor es por **tema**, no
por área: `notas-init` ofrece generar `agente/agents/profesor-<tema>.md` al
dar de alta un tema nuevo, con una persona diseñada para ese tema puntual (un
libro de literatura pide un profesor de letras, una cert pide un instructor
de esa cert); `notas-sesion` ofrece generarlo para los temas que todavía no
lo tienen. `idioma` separa el idioma de la fuente, de las notas y de los
exámenes, así
`notas-resumir` no asume inglés → español. `enlaces` son fuentes externas
(documentación oficial, un curso); `recursos/` son archivos locales (el PDF
del libro, un apunte). Los dos aparecen juntos arriba del índice del cuaderno.

Para agregar un tema: `/notas-init` entrevista y crea `temas/<slug>/` con
`tema.json` y las carpetas `notas/`, `examenes/`, `ejercicios/`, `recursos/`
y `progreso/`. Aparece solo en las listas.

## Cuaderno de notas

**Un cuaderno por tema.** No se crean notas a mano: cada **Título 1** que
escribís *es* una sección, y se guarda como su propio `.md` en
`temas/<tema>/notas/`. Borrar el título borra el archivo. Renombrarlo lo
renombra. El orden de los archivos (`01-`, `02-`…) es el orden del documento.

- El cuaderno abre con el título del tema, el subtítulo y el índice. Los tres
  se editan en el lugar; el índice se arma solo con los títulos que escribís.
- **Numeración automática**: h1 → 1, 2, 3; h2 → 1.1, 1.2; h3 → 1.1.1. Es CSS,
  no se guarda en el archivo, así que nunca queda desfasada.
- Clic en una entrada del índice lleva a la sección.
- **Atajos de escritura**: `/h1` … `/h6` al empezar un renglón lo convierten en
  título; `/p` vuelve a párrafo; `/lista` o un `- ` seguido de espacio abren una
  lista. El desplegable de la barra hace lo mismo si preferís el mouse.
- Resaltar / subrayar / tachar con color: elegís el color en la barra y después
  la acción. La paleta es el array `COLORES` arriba del script de `app/notas.html`.
- **Comentarios**: sólo sobre texto ya resaltado, subrayado o tachado. Hacés clic
  en la marca y se abre un menú con los seis colores, el campo de comentario y el
  botón de quitar la marca. La marca comentada lleva un `°`; el comentario
  aparece en un globo al pasar el mouse.
- **Referencias**: el botón abre un desplegable con todas las secciones del
  índice, numeradas y sangradas por nivel. Si tenías texto seleccionado, ese
  texto queda como enlace; si no, entra el título de la sección. También podés
  escribir `[[Nombre de la sección]]` y se convierte al cerrar el corchete. Al
  pasar el mouse levanta el contenido de la sección referenciada.
- **Imagen**: entra en el flujo del texto, centrada, donde esté el cursor.
  También podés pegarla (⌘V, sirve para capturas de pantalla) o soltarla sobre
  el documento. Clic en la imagen abre un control de ancho, de 20% a 100%.
  Al guardar, la imagen se escribe como archivo en `notas/img/` y en el `.md`
  queda sólo la referencia: `<img src="img/ae738e6a.png">`. El nombre es el
  hash del contenido, así que pegar dos veces la misma captura no duplica el
  archivo, y las que dejan de estar referenciadas se borran solas.
- **Nota al margen**: queda flotando donde la dejes, en el margen derecho, al
  50% de opacidad hasta que le pasás el mouse. Se arrastra del `⠿`. Si pegás una imagen adentro,
  tenés una imagen flotante.
- **Fuente de lectura**: Serif (Charter), Inter o JetBrains Mono, en la barra.
  Se recuerda. Las dos últimas se bajan de Google Fonts; sin internet caen a la
  fuente equivalente del sistema.
- **Modo claro / oscuro** en la barra, para toda la interfaz.
- **Dictado**: clic en el micrófono o `⌃M` (Control, no Command: macOS usa
  `⌘M` para minimizar), hablás, y lo mismo para terminar. El texto entra donde
  está el cursor. Transcribe Whisper (`large-v3-turbo`) local en la GPU, fijo en
  español, sin internet salvo la primera vez que baja el modelo (~1,6 GB). El
  modelo se cambia en `MODELO_VOZ` de `app/server.py`.
- Guarda solo, 0,9 s después de cada cambio. El estado se ve en la barra.

### Qué hay dentro de un `.md`

Markdown común (`#`, `-`, `**`, `*`, `~~`) más HTML inline para lo que el
markdown no tiene: resaltados con color, comentarios, notas al margen y
renglones en blanco (`<br>`, porque markdown no sabe representar uno). Es HTML
válido dentro de markdown, así que los archivos se abren bien en Obsidian o en
cualquier editor.

`python3 app/texto.py` verifica que la ida y vuelta HTML↔MD no pierda nada ni
mueva nada de lugar.

## Orden de los temas

`tema.json` tiene un campo `orden`. Manda en las dos listas, la de notas y la
de exámenes. El tema sin `orden` cae al final, ordenado por título. El título
no lleva número: eso es lo que ordena, no lo que se lee.

```json
{ "titulo": "Fundamentals of Software Architecture", "subtitulo": "…", "orden": 1 }
```

Se edita a mano; el editor no lo pisa al guardar.

## Por qué no hay carpetas por bloque

Los bloques son orden de lectura, no ubicación de archivos. Un tema es un
tema; agrupar carpetas por bloque obliga a moverlas si cambia el orden.
El agrupamiento vive en un `progreso/roadmap.md` dentro del tema que haga de eje.

## Skills

Viven en `agente/skills/`. Se activan solas cuando el pedido encaja, o las
llamás por nombre (`/nombre` en Claude Code). Para otro agente, ver
`/notas-setup-agente`. Todas escriben en las carpetas de este proyecto, no
en el chat.

| Skill | Para qué | Deja |
|---|---|---|
| `/notas-setup-agente` | Configurar el repo para tu agente (Claude Code, Codex, Gemini, Cline…) | Symlinks o archivos nativos, en `.git/info/exclude` |
| `/notas-sesion` | Punto de entrada: qué falta en todos los temas, qué hacer hoy | Deriva a la skill que corresponda |
| `/notas-init` | Dar de alta un tema nuevo | `temas/<tema>/` completo, `aprendizaje.md` con la Misión |
| `/notas-ensenar` | Entender algo de cero, en serio | Una lección en `temas/<tema>/notas/` |
| `/notas-resumir` | Condensar un texto que ya entendés, en el idioma del tema | Secciones nuevas en una nota existente |
| `/notas-examen` | Convertir material en preguntas corregibles | `temas/<tema>/examenes/<slug>/examen.json` |
| `/notas-ejercicios` | Forzar a producir un artefacto, no a responder | `temas/<tema>/ejercicios/<slug>/enunciado.md` |
| `/notas-correjir` | Corregir un intento de examen o de ejercicio | El `.md` de feedback junto al intento, `aprendizaje.md`, `progreso/` |
| `/notas-repasar` | Que lo entendido no se evapore | `temas/repaso/examenes/YYYY-MM-DD/examen.json` |

Más el subagente **investigador** (`agente/agents/`), que no se llama a mano:
`notas-ensenar` lo dispara para verificar un hecho antes de afirmarlo y para
relevar un tema antes de planificar.

### `/notas-ensenar` — la que vale la pena conocer

Viene del [sistema de amosblomqvist](https://github.com/amosblomqvist/learn),
adaptado a este proyecto. La idea de fondo: el cerebro no fija un hecho que no
está seguro de que sea seguro fijar. Si algo más profundo puede contradecirlo
después, hedgea y el hecho nunca aterriza. De ahí los dos principios:

1. **Primero las verdades incondicionales** — lo que se acepta tal cual, sin
   salvedades. Se fija al instante y da piso firme para construir encima.
2. **"¿Cómo podría haberlo descubierto yo?"** — nada aparece de la nada. Cada
   paso motivado, estilo 3Blue1Brown. Un hecho que se siente arbitrario no pega.

El objetivo no es recitar: es que el hecho sea *derivable* de cosas que ya
aceptás. Eso se sostiene solo; lo memorizado se pudre.

Tres fases, siempre, escalando el tamaño y nunca la forma:

1. **Sondear.** Te toma preguntas corregidas hasta encontrar el borde de lo que
   sabés — acotado por los dos lados: algo que contestás bien y algo que
   contestás mal. Si acertás todo, las preguntas eran fáciles y sube. Después te
   pregunta, abierto, qué querés entender exactamente.
2. **Planificar.** Te muestra el plan como grafo de dependencias: verdades
   incondicionales en las raíces, tu objetivo en el destino. **Para y espera tu
   visto bueno** — una raíz equivocada es barata de arreglar acá y cara a mitad
   de lección.
3. **Enseñar.** Nodo por nodo: motivar → establecer → conectar → control. Cada
   nodo se confirma con una pregunta antes de construirle algo encima.

```
/notas-ensenar acoplamiento y cohesión
```

Al final la lección queda escrita en `temas/<tema>/notas/`, con el grafo de
dependencias como fence `mermaid`, y te ofrece pasar a `notas-examen` o a
`notas-ejercicios`.

Dos cosas que conviene saber:

- **Es lento a propósito.** La fase de sondeo puede llevar diez preguntas. Ese
  es el trabajo, no el preámbulo: sin saber dónde está tu borde no hay forma de
  enseñar adentro de él.
- **El modo caveman se apaga mientras enseña.** La prosa comprimida sirve para
  responder consultas, no para construir un grafo de dependencias.

Editá `agente/skills/notas-ensenar/SKILL.md` si querés que enseñe distinto:
está escrito para una sola persona, y esa persona sos vos.

### `aprendizaje.md` — la memoria de cada tema

`/notas-ensenar` guarda en `temas/<tema>/aprendizaje.md` lo que sabe de vos **como
alumno**, y lo lee antes de sondear. Sin eso cada sesión arranca de cero. Tres
partes:

- **Misión** — por qué estudiás el tema, en concreto. Ancla todas las decisiones:
  qué enseñar después, qué recortar. Si es vaga, lo primero que hace es
  interrogarla.
- **Glosario** — un término entra **sólo cuando ya lo sabés usar**, no cuando te
  lo explicaron. Por eso es a la vez lenguaje canónico y señal de progreso.
- **Registro** — entradas numeradas de qué quedó entendido, qué sabías de antes,
  y sobre todo **qué concepción equivocada se corrigió**. Esas últimas son las
  más valiosas: predicen dónde vas a tropezar en temas vecinos, y son el material
  de repaso de mayor rendimiento.

No se escribe una entrada porque "se cubrió" un tema. Cubrir no es aprender: hace
falta evidencia.

### `/notas-repasar` — fluidez no es retención

Contestar bien al final de la lección mide **fluidez**: recuperarlo ahora, con el
tema fresco. Lo que importa es la **retención**: recuperarlo en tres semanas. Se
sienten igual desde adentro, y ahí está la trampa.

`/notas-repasar` arma un examen con dificultad deseable, con tarjetas Leitner:

- **Tarjetas** — cada pregunta rendida es una tarjeta, con caja *rápida*,
  *media* o *lenta*. Un acierto sube de caja; un fallo vuelve entera a la
  rápida. Tres aciertos seguidos en la lenta retiran la tarjeta.
- **Debilidad** — lo que falló pesa más, y las concepciones equivocadas de
  `aprendizaje.md` entran sí o sí.
- **Intercalado** — mezcla temas en la misma sesión. Un repaso de un solo
  capítulo no es un repaso, es volver a rendir.
- **Recordar, no reconocer** — reescribe los enunciados. Una pregunta vista
  textual mide si te acordás del examen, no del concepto.

```
/notas-repasar
```

Cada repaso es una carpeta fechada en `temas/repaso/examenes/`; las viejas
quedan como registro de qué se estuvo olvidando. **El espaciado depende de que
`notas-correjir` deje su fila en `progreso/log.md` de cada tema** — sin eso, la
skill queda ciega.

### De dónde salen

`/notas-ensenar` viene del sistema de [amosblomqvist](https://github.com/amosblomqvist/learn)
(el grafo de dependencias, las verdades incondicionales, el sondeo del borde).
La memoria por tema, la misión, el glosario y `/notas-repasar` vienen de la skill
`teach` de [Matt Pocock](https://github.com/mattpocock), adaptadas: su versión
asume que el directorio entero es un workspace de enseñanza con lecciones en HTML
suelto, que acá ya lo cubren el cuaderno y los exámenes.

## Formato de examen

Un examen es una carpeta, `temas/<tema>/examenes/<slug>/`, con `examen.json`
adentro. Antes de escribir preguntas, `/notas-examen` pregunta qué tipos
incluir (podés no tener micrófono, o no querer grabar oral) — nunca asume las
cuatro. Cada pregunta tiene un `tipo` (default `opcion_multiple` si no está):

```json
{
  "titulo": "FoSA — Cap 1",
  "preguntas": [
    {
      "tipo": "opcion_multiple",
      "q": "¿Pregunta?",
      "opciones": ["A", "B", "C", "D"],
      "correcta": 2,
      "explicacion": "Por qué C y por qué no las otras."
    },
    {
      "tipo": "desarrollo",
      "q": "Explicá cuándo un topic es preferible a una cola y por qué.",
      "rubrica": ["Menciona extensibilidad/acoplamiento", "Da un criterio de decisión, no solo pros/contras"]
    }
  ]
}
```

`correcta` es índice desde 0 y las preguntas de `opcion_multiple` se mezclan y
autocorrigen en el cliente, igual que siempre. `desarrollo`, `oral` y
`practico` no tienen `correcta`: tienen `rubrica`, y no hay forma de
autocorregirlas en el navegador. `oral` graba por voz (mismo mecanismo que el
dictado del cuaderno) y transcribe antes de guardar.

Al terminar, `examen.html` guarda el intento entero con `POST /api/intento` en
`examenes/<slug>/intentos/<fecha>.json`. Si el examen tenía preguntas no-MC,
corré `/notas-correjir` sobre ese intento: chequea cada punto de la rúbrica,
escribe `intentos/<fecha>.md` con el feedback y actualiza `aprendizaje.md` y
`progreso/`. La misma skill corrige los ejercicios de `/notas-ejercicios`
contra su `enunciado.md` en vez de una rúbrica.
