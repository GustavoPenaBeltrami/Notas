---
name: notas-correjir
description: Corrige un intento de examen o de ejercicio — chequea cada punto de la rúbrica o de la consigna, escribe el feedback al lado del intento, actualiza aprendizaje.md y el progreso del tema. Usar cuando el usuario dice "corregime este intento", "cómo me fue", "corregí mi ejercicio", "/notas-correjir", o después de rendir un examen con preguntas no-MC en examen.html o de entregar un ejercicio de notas-ejercicios.
---

# Corregir

Un intento sin devolución es práctica a ciegas. Esta skill cierra el loop:
compara lo que entregó contra lo que se pedía, dice qué falta (no "está mal"), y
deja todo anotado para que `notas-repasar` y la próxima sesión lo usen.

## Qué intento corregir

Un intento está **pendiente** cuando existe `intentos/<fecha>.<ext>` sin su
`intentos/<fecha>.md` compañero. Si el usuario no dice cuál, buscá en
`temas/*/examenes/*/intentos/` y `temas/*/ejercicios/*/intentos/`; si hay uno
solo, corregí ese; si hay varios, preguntá con `AskUserQuestion`.

## Dos fuentes, un mecanismo

Lo único que cambia es contra qué se compara.

**Intento de examen** — leé `examenes/<slug>/intentos/<fecha>.json` (crudo),
`examenes/<slug>/examen.json` (preguntas y rúbricas) y las `notas/*.md`
relevantes.
- `opcion_multiple`: ya viene corregida por el cliente; recalculá el score
  comparando `elegida` con `correcta` y listá las falladas con su `explicacion`.
- `desarrollo`, `practico`: contrastá la respuesta contra **cada punto**
  de la `rubrica`. Parafrasear cuenta; tocar la palabra sin el concepto no.
- `oral`: si la respuesta trae `texto` (el alumno usó el fallback escrito),
  corregila igual que `desarrollo`. Si trae `audio` (nombre de archivo en
  `intentos/`), esa es la fuente de verdad — vos no podés escuchar el archivo
  directamente, así que transcribilo con el mismo modelo que usa el servidor
  (`MODELO_VOZ` en `app/server.py`), en el idioma de `tema.json` →
  `idioma.examenes`:

  ```bash
  python3 -c "import mlx_whisper, json; print(json.dumps(mlx_whisper.transcribe(
      'temas/<slug>/examenes/<examen>/intentos/<archivo-de-audio>',
      path_or_hf_repo='mlx-community/whisper-large-v3-turbo', language='<idioma>')['text']))"
  ```

  Corregí la transcripción contra la `rubrica` igual que una respuesta escrita.
  No toques el audio. Aclará en el feedback que la transcripción no evalúa
  pronunciación ni prosodia, solo contenido.

**Intento de ejercicio** — leé `ejercicios/<slug>/enunciado.md`, el artefacto
(`ejercicios/<slug>/intentos/<fecha>.<ext>`) y las notas en las que se apoya. No
hay rúbrica: derivá los criterios de la consigna y evaluá si el artefacto **usa**
el concepto, no si "toca el tema". Un ADR que no pesa trade-offs uno contra el
otro no cumple aunque mencione las palabras correctas. Molde *enseñar*: se
corrige igual que una respuesta `oral`.

Si algo de lo que vas a afirmar como correcto no está en las notas ni en
`recursos/` y dudás aunque sea un poco, verificalo con el subagente
`investigador` antes de marcarlo.

## Qué escribís

**1. `intentos/<fecha>.md`**, al lado del intento, mismo formato para examen y
ejercicio:

```md
# Intento — <slug> — YYYY-MM-DD HH:MM

**Score MC:** 4/5 · **Rúbrica desarrollo/oral:** 2 de 3 preguntas con feedback completo

## [02] Desarrollo — trade-offs de topic vs cola
✓ Mencionó extensibilidad y acoplamiento.
✗ No mencionó el problema de seguridad (wiretap). Ver `notas/02-....md#analizando-trade-offs`.
Feedback: bien encaminado, pero la respuesta completa necesita el lado de seguridad para ser defendible en una revisión real.

## Qué mejorar
- Repasar la sección de seguridad de topics/colas antes del próximo intento.
```

- ✓/✗ por punto, cada ✗ con qué falta y la sección de la nota que lo cubre.
- En ejercicios, la línea de score es `**Criterios de la consigna:** N de M`.
- Si no hay nota que lo cubra, decilo: es un hueco de las notas, no del alumno.

**2. `aprendizaje.md` del tema** — mismas reglas de Registro que
`notas-ensenar`: entra lo que revela una **concepción equivocada** (con qué
creía y qué es) o una demostración no trivial de entendimiento. En ejercicios
pesa doble: una concepción equivocada que sobrevive hasta producir un artefacto
es más seria que una que sólo aparece en una respuesta corta. Acertar lo
esperable no se registra.

**3. Progreso del tema** — ver abajo.

## Progreso

Escribís en `temas/<tema>/progreso/` al corregir, nunca antes (un examen armado
pero no rendido no se anota).

- **`log.md`**: una fila al final de la tabla que corresponda; si la sección no
  existe, creala. No borres filas viejas.

  ```md
  ## Exámenes
  | Fecha | Examen | MC | Rúbrica | Intento |
  ## Ejercicios
  | Fecha | Ejercicio | Molde | Criterios | Intento |
  ```

  Si el examen corresponde a una fila de `## Lectura`, completá además su
  columna `Examen (nota)`. Si fue un repaso (`temas/repaso/`), anotá qué temas
  entraron: eso mueve el reloj de esas unidades, no el del tema "repaso".
- **`status.md`**: se reescribe, no se acumula. Tocalo sólo si cambió algo del
  presente (próximo examen, pendiente inmediato). No maquilles el estado.
- Fecha siempre `YYYY-MM-DD`, nunca relativa. Si falta un dato, preguntá una
  sola vez y todo junto. No inventes notas ni fechas.

## Cierre en el chat

Tres o cuatro líneas: score o criterios cumplidos, lo más flojo, y **una sola**
recomendación concreta de qué reforzar antes del próximo intento (la skill que
conviene: `notas-ensenar`, `notas-ejercicios` o `notas-repasar`).
