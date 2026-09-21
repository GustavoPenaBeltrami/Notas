---
name: notas-resumir
description: Resume un texto (pegado, adjunto, o de recursos/ del tema) y lo agrega a una nota en temas/*/notas/*.md, en el idioma que el tema tenga configurado. Usar cuando el usuario dice "resumime esto", "/notas-resumir", "agregá este resumen a la nota" o pega/adjunta un fragmento de libro/artículo para condensar.
---

# Resumir

Resume texto técnico y lo agrega a un archivo de notas existente (`temas/<tema>/notas/*.md`), siguiendo el mismo formato que ya usan esas notas.

## Datos necesarios (preguntar juntos si faltan)

1. **Origen**: de dónde sale el texto —
   - **pegado**: viene en el mensaje.
   - **adjunto**: un PDF/imagen que el usuario adjuntó — leelo con `Read`.
   - **`recursos/`**: un archivo ya guardado en `temas/<tema>/recursos/` — preguntá cuál si no lo dice.
2. **Destino**: qué tema y qué archivo de `notas/` (ej. `temas/fundamentals_software_architecture/notas/02-fundamentos-razonamiento-arquitectonico.md`). Si el usuario ya viene trabajando sobre una nota en la conversación, usar esa sin volver a preguntar.
3. **Nivel de resumen** (si no lo dice, usar `medio`):
   - **compacto**: muy compacto, solo bullets con la idea clave de cada concepto. Sin desarrollo, sin ejemplos salvo que sean imprescindibles.
   - **medio** (default): más corto que el original pero con suficiente explicación para entender el concepto sin leer el texto fuente. Incluye los ejemplos más importantes.
   - **extenso**: desarrollado, cercano a apuntes completos. Conserva matices, la mayoría de los ejemplos y las distinciones del original, pero sigue siendo un resumen (no traducción).
4. **Idioma de salida**: default `idioma.notas` de `tema.json`. Si el tema no tiene `idioma` seteado, preguntá una vez (y no de nuevo en la misma sesión).

Si ya tenés los datos (por contexto de la conversación o porque el usuario los dio), no preguntes: resumí directo.

## Antes de escribir

Mirar cómo está estructurada la nota destino (y si hace falta, `app/texto.py` / `app/server.py` para entender la convención general de `temas/*/notas/`):

- Cada `.md` en `notas/` arranca con un `# ` (h1, título de la nota) — ese h1 es lo que el editor usa para partir el archivo en secciones al guardar desde la UI. No agregues un segundo h1.
- Los temas dentro de la nota van como `##`; subtemas, como `###`.
- Listas con `- ` (guion + espacio), una idea por ítem.
- Párrafos normales para explicación en prosa.
- HTML crudo (`<img>`, `<mark>`, etc.) se deja tal cual si ya existe en la nota; no inventar marcas nuevas.
- Un fence ```` ```mermaid ```` o ```` ```math ```` se renderiza en `notas.html`. Usarlo sólo si el
  texto original describe una estructura o una fórmula que se entiende mejor
  dibujada, nunca de adorno.

## Reglas del resumen

- Escribí en el idioma de salida (arriba), natural, estilo apunte de estudio — no traducción literal, explicá la idea.
- Términos técnicos importantes se conservan en su idioma original si es distinto al de salida (con su explicación si hace falta), ej. *technical breadth*, *trade-off*, *coupling*.
- No agregar información que no esté en el texto original.
- No agregar conclusión ni repetir conceptos ya dichos.
- Si el texto trae ejemplos, conservar los más importantes (más en nivel `mucho`, menos en `poco`).
- Si parte del texto ya está cubierto en la nota (redundante con algo ya resumido antes), no lo dupliques: integralo o avisá que lo estás fusionando en vez de repetirlo.

## Cómo agregarlo

Agregar el resumen al **final** del archivo destino, como sección(es) nueva(s) (`##`/`###` según corresponda al nivel de detalle del texto pasado — un texto con subtítulos propios en inglés se traduce a subtítulos propios). Usar Edit (append al final del archivo), no reescribir lo que ya hay salvo que el usuario pida explícitamente reestructurar una parte existente.

## Después de escribir

Devolver en 1-2 líneas qué título(s) quedaron agregados y en qué archivo. No repetir el resumen completo en el chat si ya quedó escrito en el archivo.
