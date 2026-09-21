---
name: notas-examen
description: Arma un examen en JSON a partir del contenido crudo que pega el usuario (un capítulo de libro, documentación, una guía de certificación), auditando antes contra el progreso del tema. Usar cuando el usuario pega páginas, un capítulo, un PDF extraído o su propio resumen y pide un examen, un quiz, preguntas, o dice "tomame examen de esto".
---

# Notas examen

Convierte contenido crudo de estudio en un examen que consume `app/examen.html`.

## Auditoría previa (antes de escribir una sola pregunta)

Leé, en este orden:

1. `temas/<slug>/tema.json` — `tipo` (cómo se escriben las preguntas, ver abajo), `idioma.examenes`.
2. `temas/<slug>/progreso/status.md` — qué unidad está en curso, para no armar el examen sobre algo que todavía no se dio.
3. `temas/<slug>/aprendizaje.md` — el Registro: lo que ya está confirmado como piso no hace falta repreguntarlo como si fuera nuevo, y lo que quedó anotado como concepción equivocada corregida sí conviene insistirlo (es la prueba de que de verdad se corrigió).

## Dónde se escribe

`temas/<slug-del-tema>/examenes/<slug-examen>/examen.json`

- El slug de tema es el nombre de carpeta que ya existe en `temas/`. Listalas antes de escribir; no inventes carpetas nuevas.
- Un tema puede ser un libro, una certificación, documentación o un curso. Mirá el campo `tipo` de su `tema.json`: cambia cómo se escriben las preguntas (ver abajo).
- El slug de examen sigue la unidad del tema: `cap-01` para un libro, `dominio-02` para una certificación, `<servicio>` para documentación — es nombre de **carpeta**, el archivo adentro siempre se llama `examen.json`.
- Si el usuario no dice de qué tema o unidad es, deducilo del contenido. Si sigue ambiguo, preguntá una sola vez.
- Si la carpeta ya existe: preguntá si reemplazar o crear `cap-NN-b`.

## Formato

```json
{
  "titulo": "FoSA — Cap 2: Pensamiento arquitectónico",
  "preguntas": [
    {
      "tipo": "opcion_multiple",
      "q": "Enunciado.",
      "opciones": ["A", "B", "C", "D"],
      "correcta": 2,
      "explicacion": "Por qué C es correcta y por qué caen las otras tres."
    },
    {
      "tipo": "desarrollo",
      "q": "Explicá cuándo un topic es preferible a una cola y por qué.",
      "rubrica": ["Menciona extensibilidad/acoplamiento", "Menciona seguridad/wiretap", "Da un criterio de decisión, no solo lista pros/contras"]
    }
  ]
}
```

`tipo` puede ser `opcion_multiple` (default si falta, así los exámenes viejos siguen siendo válidos), `desarrollo`, `oral` o `practico`. `opcion_multiple` lleva `opciones`/`correcta`/`explicacion` como siempre. Los otros tres no llevan `correcta`: llevan `rubrica`, 3-5 puntos cortos y verificables (no una respuesta modelo única — una rúbrica permite corregir parafraseo). `oral` es igual a `desarrollo` salvo que la respuesta se captura por voz. `correcta` es índice desde 0. `opcion_multiple` siempre 4 opciones. `examen.html` mezcla las preguntas solo, no las ordenes vos.

## Qué tipos de pregunta incluir

Antes de escribir una sola pregunta, preguntá con `AskUserQuestion`
(multiSelect) qué tipos entran en este examen — no asumas que quiere las
cuatro: puede no tener micrófono o no querer grabar oral.

- Opciones: `opción múltiple`, `desarrollo`, `oral`, `práctico`.
- Preselección por default según la regla de reparto de abajo: `opción
  múltiple` y `desarrollo` marcados; `oral` y `práctico` sin marcar, salvo que
  el tema sea claramente práctico/oral (`tipo: "práctica"`, o un idioma), en
  cuyo caso marcalos también por default.
- Repartí sólo entre los tipos que confirmó. Si eligió uno solo, el examen es
  100% de ese tipo.
- `oral` se responde grabando audio (mismo mecanismo que el dictado del
  cuaderno); `notas-correjir` corrige sobre la transcripción, igual que
  `desarrollo`.

## Cómo se escriben las preguntas

10 a 15 preguntas por capítulo. Repartidas así:

- ~30% definición y vocabulario preciso del capítulo.
- ~40% aplicación: un escenario concreto, qué corresponde hacer.
- ~30% trade-offs y contraejemplos: qué se paga por elegir X, cuándo X es la opción equivocada.

Sesgá a aplicación y trade-off. El objetivo es entender, no recitar.

**Reparto de tipos**: entre los tipos confirmados en la pregunta de arriba,
default 60% `opcion_multiple` / 40% `desarrollo` cuando ambos están
incluidos. Si `oral`/`practico` también están incluidos, sumalos repartiendo
desde el 40% no-MC en vez de agregar porcentaje nuevo.

**Según el `tipo` del tema:**

- `libro` — el reparto de arriba tal cual.
- `certificación` — imitá el examen real. Para AWS Cloud Practitioner (CLF-C02):
  opción múltiple con una correcta y tres distractores, o respuesta múltiple con
  dos correctas de cinco opciones. Preguntas de escenario corto, no de definición.
  Respetá el peso de cada dominio si armás un simulacro completo.
- `documentación` — preguntas sobre cuándo usar qué y qué límites tiene, no sobre
  nombres de parámetros. La documentación se consulta; lo que hay que saber de
  memoria es el criterio de elección.
- `curso` — seguí la unidad del curso.

### Cómo se construyen las opciones (`opcion_multiple`)

Que las opciones queden parejas no se logra auditando al final: para entonces la
pista ya está adentro. Construilas de modo que la paridad salga sola.

1. **Toda opción es una afirmación pelada, sin justificación.** La pista número
   uno es que la correcta venga con su propio razonamiento ("…, porque preserva el
   acoplamiento bajo") mientras las otras tres van peladas: queda más larga y más
   específica. Cero "porque" en las opciones — todo el razonamiento va en
   `explicacion`, que aparece recién después de contestar.
2. **Escribí primero la afirmación correcta y después mutála en cada distractor.**
   Tomá una confusión real o un vecino fácil de confundir y escribí lo que
   afirmaría alguien que la tiene, con el *mismo* esqueleto, el mismo grano y el
   mismo registro. Así las cuatro opciones son "la afirmación bajo alguna
   creencia" y la correcta es la afirmación bajo la creencia correcta. El
   paralelismo sale por construcción en vez de tener que vigilarlo.
3. Cada distractor tiene que ser un error que él podría cometer de verdad — así
   cuál elige es diagnóstico — pero inequívocamente incorrecto: tentador, no
   tramposo.
4. **Nada de negritas asimétricas.** No resaltes el concepto que estás evaluando
   sólo en la correcta: eso lo delata al instante. O nada en negrita, o el término
   paralelo en las cuatro.

Si leyendo las cuatro en frío podés adivinar cuál es sin saber el tema, te
saltaste el paso 1 o el 2: regeneralo, no lo parchees.

Reglas de calidad, no negociables:
- Distribuí `correcta` entre 0, 1, 2 y 3. No la dejes concentrada en un índice.
- Prohibido: "todas las anteriores", "ninguna de las anteriores", "A y C", dobles negaciones.
- Una pregunta evalúa una sola idea.
- La `explicacion` dice por qué la correcta lo es **y** qué confusión representa cada distractor. Es la parte que enseña: si es una sola línea genérica, está mal escrita.
- Todo sale del contenido que pegó el usuario. Si algo hace falta y no está en el material, no lo inventes: señalalo aparte.

### Cómo se escribe la `rubrica` (`desarrollo`/`oral`/`practico`)

3 a 5 puntos cortos, cada uno **verificable** en la respuesta (algo que se puede
marcar ✓/✗ leyéndola), no una respuesta modelo. Un punto de rúbrica nombra un
concepto o un criterio concreto ("menciona el problema de seguridad/wiretap"),
nunca algo vago ("entiende bien el tema"). Igual que en `opcion_multiple`, todo
sale del contenido que pegó el usuario.

## Diagramas y fórmulas en las preguntas

`examen.html` renderiza fences dentro de `q`, de cada opción y de `explicacion`.
Sirve para preguntas de arquitectura ("dado este diagrama, ¿qué falla?") y para
percentiles y complejidad.

```json
{
  "q": "Dado el flujo:\n\n```mermaid\ngraph LR\n  A[API] --> B[(DB)]\n```\n\n¿Dónde está el acoplamiento temporal?",
  "explicacion": "..."
}
```

Van como texto dentro del string JSON, así que los saltos de línea son `\n` y en
`math` las barras de LaTeX se escapan dobles (`\\frac`). Usalos sólo cuando el
dibujo aporta algo que la prosa no: un diagrama decorativo suma ruido y una chance
más de estar equivocado.

## Después de escribir

1. Validá el JSON: `python3 -m json.tool temas/<slug>/examenes/<slug-examen>/examen.json > /dev/null`
2. Para cada pregunta `opcion_multiple`: verificá que `correcta` esté entre 0 y 3 y que
   tenga 4 opciones, y que `correcta` no quede concentrada en un índice. Para cada
   `desarrollo`/`oral`/`practico`: verificá que tenga `rubrica` con 3-5 puntos.
3. Decile al usuario la ruta y que lo abra con `npm run exam`.
4. Si el examen tiene preguntas no-MC, avisale que al rendirlo va a necesitar
   correr `notas-correjir` sobre el intento — `examen.html` no puede corregir
   `desarrollo`/`oral`/`practico` solo.
5. No anotes nada en `progreso/log.md` al crear el examen: eso lo hace
   `notas-correjir` cuando el usuario rinde y corrige el intento, no antes.

Para un repaso espaciado que mezcla temas en vez de un examen de un capítulo,
la skill es `notas-repasar`, que reusa estas mismas reglas de construcción.
