---
name: notas-repasar
description: Arma un repaso espaciado e intercalado con tarjetas Leitner — mezcla temas, prioriza lo que falló o está en caja rápida, y reescribe las preguntas para que haya que recordar y no reconocer. Usar cuando el usuario dice "repasar", "/notas-repasar", "hace cuánto que no veo esto", "se me está olvidando", "tomame repaso", o cuando terminó un bloque y conviene consolidar antes de seguir.
---

# Notas repasar

Contestar bien al final de una lección mide **fluidez**: poder recuperarlo ahora,
con el tema fresco. Lo que importa es la **retención**: poder recuperarlo en tres
semanas. Se sienten igual desde adentro, y ahí está la trampa — la fluidez da una
sensación de dominio que la retención todavía no respalda.

La retención no se construye repitiendo, se construye con dificultad deseable.
Esta skill produce esa dificultad de tres formas, y las tres son obligatorias:

- **Recuperar, no reconocer.** Una pregunta que ya vio textual mide si se acuerda
  del examen, no del concepto.
- **Espaciar.** Lo que hace meses que no toca vale más que lo de ayer.
- **Intercalar.** Temas mezclados en la misma sesión, nunca agrupados.

## Dónde escribe

`temas/repaso/examenes/YYYY-MM-DD/examen.json` (misma estructura de carpeta que
cualquier examen — ver `notas-examen`). Los intentos van en
`temas/repaso/examenes/YYYY-MM-DD/intentos/`, igual que en cualquier otro tema.

Es un tema más: si `temas/repaso/` no existe, creá la carpeta con este
`tema.json` y con `examenes/` adentro. Aparece solo en las dos listas.

```json
{ "titulo": "Repaso", "subtitulo": "Espaciado e intercalado", "tipo": "repaso", "orden": 0, "enlaces": [] }
```

El formato del examen es el de `notas-examen`, y **sus reglas de construcción de
opciones aplican enteras** — sobre todo escribir primero la afirmación correcta y
mutarla en cada distractor. No las repitas acá: leé esa skill.

## De dónde sale el material

En este orden:

1. **`temas/*/progreso/log.md`** — qué rindió cada tema, cuándo y con qué nota.
2. **`temas/*/examenes/*/intentos/*.json`** — intentos individuales, con el
   detalle de qué pregunta se acertó o falló. Es la evidencia de la que se
   derivan las cajas Leitner (ver abajo) — no hace falta un archivo de estado
   de tarjeta aparte.
3. **`temas/*/examenes/*/examen.json`** — el banco de preguntas ya escritas.
4. **`temas/*/aprendizaje.md`** — el registro. Las **concepciones equivocadas
   corregidas** son el material de repaso más valioso que hay: una creencia
   incorrecta desalojada tiende a volver. Buscalas y apuntales.
5. **`temas/*/notas/*.md`** — si un tema todavía no tiene exámenes, las preguntas
   salen de la nota.

## Cómo se elige qué entra — tarjetas Leitner

Cada pregunta (de cualquier `examen.json` del banco, de cualquier tema) es una
**tarjeta**. No tiene archivo de estado propio: su caja se recalcula cada vez que
se arma un repaso, a partir de la evidencia en `temas/*/examenes/*/intentos/*.json`
y `temas/*/progreso/log.md`.

**Cajas**: *rápida* (nueva, o falló la última vez), *media*, *lenta* (varios
aciertos seguidos). Con cada acierto consecutivo sube una caja. Con **un solo
fallo vuelve entera a rápida** — no medio paso atrás, un fallo es señal fuerte.

**Retiro**: tras **3 aciertos consecutivos en la caja lenta**, la tarjeta se
retira de la rotación activa. No se pierde: pasa al repaso ambulatorio semanal.

**Qué entra a un repaso normal**: apuntá a 12-15 preguntas, priorizando caja
rápida > media > lenta, y dentro de cada caja las que hace más tiempo no se ven
en `progreso/log.md`. Si no hay evidencia de nada (tema recién empezado o sin
intentos), tratá todo como caja rápida y repartí parejo.

**Repaso ambulatorio semanal**: cuando un tema se queda sin tarjetas activas
(todo retirado a lenta), no se abandona — una vez por semana hacele un repaso
oral/chat corto de todo el set retirado, sin guardarlo como examen (no es
reproducible ni bancable). Si lo pasa, el set queda confirmado otra semana más.
Si falla algo puntual, esa tarjeta vuelve a caja rápida y entra en el próximo
repaso normal.

**Debilidad**: dentro de la caja rápida, lo que figure como concepción
equivocada corregida en `aprendizaje.md` entra sí o sí.

**Intercalado.** El resultado mezcla temas. `examen.html` ya mezcla las preguntas
al rendir, así que no las ordenes vos — pero **sí** asegurate de que el conjunto
tenga al menos dos temas distintos cuando haya material de dos temas. Un repaso
de un solo capítulo no es un repaso, es volver a rendir.

**Alternativa documentada, no implementada**: el sistema anterior por
intervalos fijos crecientes (1 → 3 → 7 → 16 → 35 → 90 días desde la última vez
rendido) queda como método alternativo si Leitner no alcanza — no correr los dos
motores en paralelo. SM-2/FSRS quedan en backlog, sin investigar todavía.

## Cómo se reescriben las preguntas

Nunca copies una pregunta del banco tal cual. Reusá la **idea**, reescribí el
**enunciado**:

- Cambiá el escenario. Si la original preguntaba por un servicio de pagos,
  preguntá por uno de inventario.
- Cambiá la dirección. Si daba el concepto y pedía la definición, dá la situación
  y pedí el concepto.
- Subí un escalón cuando puedas: de "qué es X" a "acá hay dos opciones, cuál y
  por qué". Reconocer es más fácil que aplicar, y queremos lo difícil.
- Rotá cuál es la correcta. Si en el examen original era la B, que acá no lo sea.

Si una pregunta sólo se puede hacer de una forma, dejala — pero que sean pocas.

## Después de escribir

1. Validá: `python3 -m json.tool temas/repaso/examenes/<fecha>/examen.json > /dev/null`.
2. Chequeá que `correcta` esté entre 0 y 3, que todas tengan 4 opciones, y que el
   índice correcto esté repartido.
3. Decile la ruta y que lo abra con `npm run app`.
4. Contale en dos líneas **por qué entró cada tarjeta**: "seis de DDIA cap 3, en
   caja rápida por un fallo la semana pasada; cuatro de FoSA cap 2, recién
   entrando; dos de AWS para intercalar". El repaso enseña más cuando se entiende
   su criterio.
5. Cuando lo rinda, escribí vos mismo la fila de repaso en
   `temas/<tema>/progreso/log.md` de cada tema que entró (una fila por tema, no
   una fila en el "tema" repaso) — fecha `YYYY-MM-DD`, nunca relativa. Es lo que
   alimenta las cajas la próxima vez: sin ese registro, esta skill queda ciega.

## Lo que no hace

No borra ni toca los exámenes originales: son el banco, y su historial en
`log.md`/`intentos/` es lo que hace funcionar el espaciado. Cada repaso es una
carpeta nueva, fechada. Las viejas quedan, y son un registro de qué se estuvo
olvidando.
