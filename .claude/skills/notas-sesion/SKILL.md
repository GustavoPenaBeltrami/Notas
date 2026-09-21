---
name: notas-sesion
description: Punto de entrada de una sesión de estudio — releva el estado de todos los temas (repasos vencidos, intentos sin corregir, temas sin ejercicios, tema.json incompletos), pregunta qué quiere hacer hoy y deriva a la skill que corresponda. Usar cuando el usuario dice "arranquemos", "qué estudio hoy", "qué tengo pendiente", "/notas-sesion", "quiero registrar que…", o abre una sesión sin pedido concreto.
---

# Sesión

Orquesta, no anota. Esta skill no escribe en `progreso/`: cada skill que produce
un evento (`notas-ensenar`, `notas-correjir`, `notas-repasar`) escribe el suyo.
Si el usuario viene a "registrar que terminó el capítulo X", derivalo a la skill
que corresponde a ese evento, o actualizá `status.md` del tema con las reglas de
`notas-ensenar` si fue sólo lectura.

## 1. Relevar (sin preguntar nada todavía)

Leé del filesystem, no de memoria:

- `temas/*/tema.json` y `temas/*/progreso/status.md` — qué hay y en qué unidad
  está cada tema.
- **Intentos sin corregir**: todo `temas/*/{examenes,ejercicios}/*/intentos/<fecha>.<ext>`
  (`.json` en exámenes; cualquier extensión en ejercicios) sin su
  `<fecha>.md` compañero. Ojo: en ejercicios el artefacto puede ser `.md`; es
  pendiente si es el único archivo con esa fecha.
- **Repasos vencidos**: aplicá el criterio de cajas Leitner de `notas-repasar`
  (leé esa skill, no lo reimplementes distinto) sobre `temas/*/progreso/log.md`
  e intentos. Contá también temas con todo retirado cuyo repaso ambulatorio
  semanal esté vencido.
- **Temas con notas pero cero ejercicios** (`notas/*.md` existe y `ejercicios/`
  está vacío o no existe). Es una señal a mostrar: leer sin producir no cierra
  el loop.
- **`tema.json` incompletos**: `objetivos` vacío/ausente o `motivo`
  vacío/ausente.
- **Temas sin agente-profesor**: por cada `temas/<slug>/`, chequeá si existe
  `.claude/agents/profesor-<slug>.md`. Los que no lo tengan, listalos — es una
  señal a mostrar, no un bloqueo.

Mostrá el resumen en pocas líneas, agrupado por tema, sólo lo que tenga algo.

## 2. Completar tema.json si falta

Si algún tema tiene `objetivos` o `motivo` vacíos, ofrecé completarlos ahora
(una pregunta abierta por campo, sin corregir). Si acepta, escribilos en
`tema.json` y, si `aprendizaje.md` tiene la Misión vacía, completala con lo
mismo. Si no acepta, seguí: no bloquea la sesión.

Para cada tema sin `.claude/agents/profesor-<slug>.md` (relevado en el paso
1), ofrecé generarlo con el mismo criterio de `notas-init` §4 (persona
diseñada para ese tema puntual, default sí, plantilla y chequeo de esa
sección). Uno por vez si son varios; no bloquea la sesión si dice que no.

## 3. Preguntar el objetivo de la sesión

Con `AskUserQuestion`, en una sola tanda:

- **Tema(s)** — uno o varios; sugerí primero los que tienen pendientes.
- **Qué hacer**:

| Opción | Deriva a |
|---|---|
| Leer / resumir | `notas-resumir` |
| Que me enseñen algo puntual | `notas-ensenar` |
| Rendir examen | `notas-examen` (o `examen.html` si ya existe) |
| Hacer un ejercicio aplicado | `notas-ejercicios` |
| Corregir un intento pendiente | `notas-correjir` |
| Repasar | `notas-repasar` |
| Revisar notas existentes | abrir `temas/<tema>/notas/` en la app |
| Dejalo, yo sigo solo | nada |

## 4. Derivar

Invocá la skill elegida pasándole lo ya reunido (tema, unidad en curso, intento
pendiente concreto, concepción equivocada relevante). No repreguntes lo que ya
se preguntó acá.

Si el destino es "Que me enseñen algo puntual" y el tema tiene
`.claude/agents/profesor-<slug>.md`, invocá ese agente (`Agent`,
`subagent_type: profesor-<slug>`) en vez de correr `notas-ensenar` en la
sesión principal — el agente sigue el mismo proceso, con más carácter de
dominio.

Si dice "dejame solo" o "yo sigo", no hagas nada más. No fuerces flujo.
