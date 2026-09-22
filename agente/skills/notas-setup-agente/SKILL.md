---
name: notas-setup-agente
description: Configura este proyecto para el agente que lo está usando (Claude Code, Codex, Gemini CLI, Antigravity, Cline, Cursor, opencode, o cualquier otro, con modelo en la nube o local vía Ollama) — expone las skills y agentes de agente/ en el formato nativo del agente, sin tocar nada versionado. Usar la primera vez que se abre el repo con un agente nuevo, o cuando el usuario dice "configurá el proyecto", "instalá las skills", "/notas-setup-agente".
---

# Setup del agente

La fuente única es `agente/`: `agente/skills/<nombre>/SKILL.md` y
`agente/agents/<nombre>.md`. Esta skill no la copia ni la reescribe: la
**expone** en el lugar donde tu herramienta la busca. Todo lo que crees es
local del usuario.

## 1. Identificate

Sabés qué herramienta sos. Si no estás seguro (o el usuario va a usar otra),
preguntá con `AskUserQuestion`. Después buscá en la documentación **actual** de
esa herramienta — no de memoria, cambia seguido — tres cosas:

1. Qué archivo de instrucciones lee al abrir el repo (`AGENTS.md`, `CLAUDE.md`,
   `GEMINI.md`, una carpeta de reglas…).
2. Si soporta skills en formato `SKILL.md`, y en qué carpeta del proyecto.
3. Si soporta subagentes definidos en archivos, y en qué carpeta y formato.

Punto de partida, a verificar:

| Herramienta | Instrucciones | Skills | Subagentes |
|---|---|---|---|
| Claude Code | `CLAUDE.md` (con `@AGENTS.md` adentro) | `.claude/skills/` | `.claude/agents/` |
| Codex | `AGENTS.md` | `.agents/skills/` | — |
| Gemini CLI | `GEMINI.md` o `contextFileName: AGENTS.md` | `.gemini/skills/` | — |
| Otras (Antigravity, Cline, Cursor, opencode) | Suelen leer `AGENTS.md` o una carpeta de reglas | Ver su doc | Ver su doc |

Ollama no es un agente: corre el modelo detrás de uno de estos. Configurá el
agente, no Ollama. Avisale al usuario que un modelo local chico puede no
sostener skills largas como `notas-ensenar`.

## 2. Exponé, en este orden de preferencia

1. **Nada que hacer** — la herramienta lee `AGENTS.md` y con eso alcanza para
   cargar las skills a mano (ver `AGENTS.md`). Si no soporta skills nativas,
   quedate acá.
2. **Symlink** — la herramienta soporta `SKILL.md`: enlazá su carpeta a la
   fuente, así nunca se desincroniza.
   ```sh
   mkdir -p .claude && ln -s ../agente/skills .claude/skills && ln -s ../agente/agents .claude/agents
   ```
   Si el formato de subagentes difiere (frontmatter distinto), enlazá sólo las
   skills y dejá los agentes al paso 3.
3. **Conversión** — sólo para lo que no entra con symlink. Generá los archivos
   en el formato nativo desde `agente/`, uno por skill o agente. Poné arriba de
   cada generado una línea que diga de qué archivo sale, y avisale al usuario
   que si edita `agente/` tiene que volver a correr esta skill.
4. **Instrucciones** — si la herramienta no lee `AGENTS.md`, creá su archivo de
   instrucciones con una sola línea que lo importe o que diga "Leé `AGENTS.md`".

Nunca edites `agente/`, `AGENTS.md` ni nada versionado para adaptarlo a tu
herramienta: la traducción de nombres de herramientas ya está en `AGENTS.md`.

## 3. Ignorá lo creado, sólo para este usuario

Agregá cada ruta que creaste a `.git/info/exclude` (no a `.gitignore`: el
repo lo comparten personas con otros agentes). Chequeá que no esté ya.

```sh
git check-ignore -v <ruta>   # debe salir .git/info/exclude
git status --short           # no debe aparecer nada nuevo
```

## 4. Verificá

- Tu herramienta lista `notas-sesion` (o, en el nivel 1, podés leer
  `agente/skills/notas-sesion/SKILL.md`).
- `git status --short` no muestra nada que no estuviera antes.

Cerrá con un resumen de tres líneas: qué nivel usaste, qué rutas creaste, y
"arrancá con `notas-sesion`". Si la herramienta necesita reiniciarse para ver
las skills, decilo.
