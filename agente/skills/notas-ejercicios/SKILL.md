---
name: notas-ejercicios
description: Arma un ejercicio aplicado sobre un tema — obliga a producir un artefacto (código, ADR, crítica, explicación) en vez de responder preguntas. Usar cuando el usuario dice "quiero un ejercicio", "hacer algo práctico de esto", "aplicar lo que aprendí", "/notas-ejercicios", o cuando notas-sesion detecta un tema con notas pero sin ejercicios.
---

# Ejercicios

Un examen evalúa si algo quedó entendido. Un ejercicio obliga a **usar** el
concepto para producir algo nuevo. Es la diferencia entre reconocer/recordar y
razonar con. Esta skill arma la consigna; la corrección es de `notas-correjir`.

## Dónde escribe

```
temas/<tema>/ejercicios/<slug-ejercicio>/
  enunciado.md
  intentos/            # acá entrega el usuario
```

`<slug-ejercicio>` en kebab-case, descriptivo (`adr-topic-vs-cola`). Si
`ejercicios/` no existe en el tema, creala.

## Proceso

1. **Leé el contexto**: `tema.json` (`tipo`, `idioma`), `progreso/status.md`
   (unidad en curso), `aprendizaje.md` y las notas de esa unidad. Mirá
   `ejercicios/` para no repetir un ejercicio ya hecho.
2. **Apuntá**: a lo último aprendido o a una **concepción equivocada corregida**
   del Registro — ejercitarla produciendo algo es la prueba de fuego de que de
   verdad se corrigió. No ejercites lo ya sólido como si fuera nuevo.
3. **Elegí el molde** que mejor fuerce el uso del concepto, no el más fácil de
   armar:
   - **aplicar** — usar el concepto en un caso concreto.
   - **construir** — producir un artefacto de cero: código, diagrama, documento
     de decisión.
   - **criticar** — dado un diseño/código ajeno (real o armado para el
     ejercicio), señalar qué está mal y por qué, con el vocabulario del tema.
   - **enseñar** — explicar el concepto de cero a un tercero hipotético
     (Feynman), escrito o grabado.

   Guía: `documentación`/`curso` de herramienta → *construir*; `libro` de
   arquitectura → *aplicar*/*criticar*; idioma → *enseñar* hablado. Si no es
   obvio, preguntá con `AskUserQuestion`.
4. **Ofrecé, no fuerces, el caso real**: si el molde es *aplicar* o *criticar*,
   preguntá si quiere usar algo de su trabajo. Si dice que no o no aplica,
   inventá un caso igual de concreto. Nunca bloquea el ejercicio.
5. **Escribí `enunciado.md`**, en el idioma `idioma.examenes` del tema:

   ```md
   # Ejercicio — ADR real de topic vs cola

   **Molde:** construir · **Tema:** FoSA cap 2 · **Se apoya en:** notas/02-...md#analizando-trade-offs

   Elegí una integración asíncrona real (del trabajo, o inventada si no tenés una a mano)
   entre dos servicios. Escribí un ADR completo decidiendo topic vs cola, con al menos dos
   trade-offs pesados explícitamente uno contra el otro. No alcanza con listar pros/contras:
   tiene que quedar una decisión y por qué la otra opción se descartó.

   **Entregá:** un `.md` con el ADR.
   ```

   Regla dura: resultado verificable. Nunca "aplicá lo que viste" ni "pensá
   sobre esto"; siempre algo con una decisión tomada, un código que corre, una
   lista de fallas justificadas. Las condiciones de la consigna son los
   criterios con los que después se corrige: escribilas para que se puedan
   chequear una por una.
6. **Cerrá** diciendo dónde entregar y qué sigue:
   - `temas/<tema>/ejercicios/<slug>/intentos/<YYYY-MM-DDTHHmm>.<ext>` — `.md`
     para ADR/crítica/explicación, la extensión del lenguaje si es código, `.md`
     con la transcripción si fue oral (vía `/api/voz`).
   - Cuando lo entregue, `notas-correjir` da el feedback y anota el progreso.
     Esta skill no escribe en `progreso/`: un ejercicio sin entregar no es un
     evento.
