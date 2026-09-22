---
name: notas-init
description: Da de alta un tema de estudio nuevo — entrevista para completar tema.json, crea la estructura de carpetas y el progreso, escribe aprendizaje.md con la Misión, hace un diagnóstico de nivel en la terminal y ofrece generar el agente-profesor dedicado al tema. Usar cuando el usuario dice "quiero empezar a estudiar X", "creá un tema nuevo", "agregá un tema", "/notas-init".
---

# Alta de tema

Un tema es una carpeta autocontenida en `temas/<slug>/`. Esta skill la deja
lista para que la primera sesión arranque con la misión clara y el nivel ya
medido.

## 1. Entrevistar

Con `AskUserQuestion`, en pocas tandas. Todos los campos son **obligatorios de
preguntar** (aunque la respuesta pueda ser "ninguno"):

- `titulo`, `subtitulo`.
- `tipo`: `libro`, `certificación`, `documentación`, `curso` o `práctica`.
- `area`: **antes de preguntar**, listá las `area` que ya existen en
  `temas/*/tema.json` y ofrecelas como opciones. Libre texto pero canónico, en
  kebab-case: no crees `arquitectura_de_software` si ya existe
  `arquitectura-software`.
- `objetivos` (1-3, concretos: "poder justificar X por trade-offs", no
  "entender X") y `motivo` (qué cambia en su trabajo o su vida cuando lo tenga).
  Si vienen vagos, repreguntá hasta que sean concretos: son la Misión.
- `idioma`: `fuente`, `notas`, `examenes`.
- `rutina` (`cadencia`, `sesion`) y `fecha_fin` (YYYY-MM-DD: para cuándo quiere terminar).
- `enlaces` y recursos locales iniciales.

`slug` de carpeta: snake_case del título, como los existentes
(`fundamentals_software_architecture`). Si ya existe, frená y preguntá.
`orden`: el siguiente libre.

## 2. Generar el filesystem

```
temas/<slug>/
  tema.json
  aprendizaje.md
  recursos/  notas/  examenes/  ejercicios/
  progreso/status.md  progreso/log.md
```

```json
{
  "titulo": "…", "subtitulo": "…", "tipo": "libro", "area": "…", "orden": 4,
  "objetivos": ["…"], "motivo": "…",
  "idioma": { "fuente": "en", "notas": "es", "examenes": "es" },
  "rutina": { "cadencia": "…", "sesion": "…" }, "fecha_fin": "YYYY-MM-DD",
  "enlaces": [{ "titulo": "…", "url": "…" }]
}
```

`progreso/status.md`:

```md
# Status — <titulo>
**Actualizado:** YYYY-MM-DD
- **Unidad en curso:** —
- **Resumen escrito:** no
- **Próximo examen:** —
## Pendiente inmediato
- [ ] …
```

`progreso/log.md`:

```md
# Log — <titulo>
## Lectura
| Fecha | Unidad | Resumen | Examen (nota) |
|-------|--------|---------|---------------|
## Repaso
| Fecha | Qué repasé | Resultado |
|-------|------------|-----------|
```

`aprendizaje.md`: el formato de `notas-ensenar` (Misión / Glosario / Registro),
con la **Misión ya escrita** desde `motivo` + `objetivos` (y qué queda fuera de
alcance si lo dijo), Glosario vacío, y el Registro con lo del paso 3. Así la
primera sesión de `notas-ensenar` no vuelve a preguntarla.

Fechas siempre `YYYY-MM-DD`. No inventes datos que no dio: campo vacío antes que
inventado.

## 3. Diagnóstico ambulatorio

En la terminal, sin guardar `examen.json`: es para ubicar el nivel, no es
reproducible ni bancable.

- Usá la mecánica de sondeo de `notas-ensenar` fase 1a — preguntas corregidas
  con `AskUserQuestion`, corrección en el mensaje siguiente, búsqueda binaria
  del borde acotado por los dos lados, mismas reglas de construcción de
  opciones — pero sobre el **nivel general del tema**, no una lección puntual.
  Unas 5-8 preguntas alcanzan; si el tema es totalmente nuevo para él, 2-3 que
  lo confirmen.
- Si dudás de un hecho de las preguntas, verificalo con `investigador`.
- Anotá el resultado en el `Registro` de `aprendizaje.md`: qué declaró saber y
  con qué profundidad, dónde quedó el borde, y cualquier concepción equivocada
  que haya aparecido.

## 4. Agente-profesor del tema

Un agente por **tema**, no por área: cada tema tiene su propia persona,
diseñada para calzar con su contenido real, no una plantilla genérica de
área — un libro de literatura pide un profesor de letras/lengua española,
*Fundamentals of Software Architecture* pide un arquitecto senior que enseña,
una certificación de AWS pide un instructor de esa cert. Es opcional: una
forma de correr `notas-ensenar` con más carácter de dominio. La memoria sigue
en `aprendizaje.md` del tema; el agente no acumula memoria propia. `area`
sigue existiendo en `tema.json` como dato de contexto/tono (§2.1 de
`plan.md`), ya no acota el alcance del agente.

1. Si ya existe `agente/agents/profesor-<slug-tema>.md`, no hay nada que
   hacer.
2. Si no existe, ofrecelo con `AskUserQuestion`, **default sí** — no lo
   asumas implícito, pero tampoco lo enfríes con "¿querés uno?" sin sesgo: es
   el default esperado.
3. Si acepta, diseñá la persona **para este tema puntual**: mirá
   `titulo`/`subtitulo`/`tipo` recién completados y elegí quién enseñaría esto
   en la vida real. Nunca un genérico "profesor de <área>".
4. Escribí `agente/agents/profesor-<slug-tema>.md`, frontmatter igual a
   `investigador.md` (`name`/`description`/`tools`/`model`):

```md
---
name: profesor-<slug-tema>
description: <persona concreta> especialista en <título del tema>. Enseña este tema siguiendo notas-ensenar, con el tono y criterio de <quién>. Usar para lecciones, explicaciones o correcciones del tema "<slug-tema>".
tools: Read, Grep, Glob, Write, Edit, WebSearch, WebFetch
model: inherit
---

Sos <persona concreta>: <2-3 oraciones sobre qué domina, qué vocabulario usa
y qué criterio aplica — anclado en este tema puntual, no en un área genérica>.

Trabajás en contexto aislado: todo lo que sabés de la persona está en la
tarea que te pasaron y en `temas/<slug-tema>/aprendizaje.md`. Leelo siempre
antes de enseñar.

## Cómo enseñás

Seguí `agente/skills/notas-ensenar/SKILL.md` entero: los dos principios,
sondear → planificar → enseñar, reglas de preguntas corregidas, dónde queda
la lección. No es un proceso paralelo: es el mismo con tu personalidad.

- **Nunca des la respuesta antes de que la intente.** Preguntá qué probó,
  dónde se trabó, y guialo a descubrirla — nunca la resuelvas vos primero.
- **Nunca de memoria.** Todo hecho dudoso se verifica con el subagente
  `investigador` antes de decirlo.
- Trampas típicas de este tema: <1-2 concepciones equivocadas frecuentes, si
  las hay>.

## Qué no hacés

No escribís fuera de `temas/<slug-tema>/`. No inventás fuentes. No das la
respuesta antes de que la intente.
```

5. **Chequeo rápido antes de guardar** (4 preguntas, no lo satures):
   - ¿La persona es específica de este tema, no de un área genérica?
   - ¿Prohíbe explícitamente resolver antes de que el alumno intente?
   - ¿Ata la verificación de hechos a `investigador`, nunca a memoria?
   - ¿Usa `aprendizaje.md` del tema como memoria, sin duplicar estado propio?
6. **Temas existentes sin profesor**: si en `temas/*/tema.json` hay otros
   temas ya dados de alta sin `agente/agents/profesor-<slug>.md`, no hace
   falta resolverlo acá — `/notas-sesion` los detecta al relevar estado y los
   ofrece con el mismo criterio, así los temas viejos lo consiguen sin volver
   a correr `notas-init` para cada uno.

**Base pedagógica del punto 4** (investigado antes de escribir la plantilla,
no a ciego): el tutor socrático de Khanmigo nunca resuelve — pregunta qué
probó el alumno y lo guía a descubrirlo; *study mode* de OpenAI maneja carga
cognitiva con preguntas escalonadas en vez de la respuesta directa; el modo
*Learning* de Claude hace una pregunta exploratoria por vez antes de
responder. Los tres coinciden en la regla que quedó arriba: nunca dar la
respuesta antes del intento.

**Fuentes**: [Khanmigo — enfoque socrático](https://aicompetence.org/ai-socratic-tutors/),
[OpenAI — Introducing study mode](https://openai.com/index/chatgpt-study-mode/),
[Claude Learning Mode vs ChatGPT Study Mode (Tom's Guide)](https://www.tomsguide.com/ai/claudes-new-learning-modes-take-on-chatgpts-study-mode-heres-what-they-do).

## 5. Cerrar

Mostrá en pocas líneas dónde quedó todo, qué salió del diagnóstico, y **un**
primer paso sugerido: leer y `notas-resumir`, o directo a `notas-ensenar` si ya
tiene base.
