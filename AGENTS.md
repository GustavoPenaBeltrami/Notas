# Notas — instrucciones para el agente

Este repo es un sistema de estudio: skills y agentes (`agente/`), un filesystem
de temas (`temas/<slug>/`) y una app local (`npm run app`). Vos sos la tercera
ventana: el usuario estudia en una, rinde y toma notas en la app, y te habla a
vos en esta.

## Primera vez

Si tu herramienta todavía no ve las skills de `agente/skills/` como propias,
leé `agente/skills/notas-setup-agente/SKILL.md` y seguilo. Deja el proyecto
configurado para vos sin tocar nada versionado.

## Skills

Cada skill es `agente/skills/<nombre>/SKILL.md` (formato Agent Skills:
frontmatter `name` + `description`, instrucciones abajo). Si tu herramienta no
carga skills sola, cuando el pedido encaje con una `description`, leé ese
`SKILL.md` entero y seguilo. La puerta de entrada es `notas-sesion`.

Los agentes de `agente/agents/*.md` son subagentes: `investigador` y un
`profesor-<tema>` por tema. Sin subagentes, leé el archivo y hacé su trabajo
vos mismo, en un paso aparte.

## Nombres de herramientas

Las skills nombran herramientas de Claude Code. Traducilas a las tuyas:

| En la skill | Qué significa |
|---|---|
| `AskUserQuestion` | Preguntar con opciones. Sin esa herramienta: pregunta numerada en el chat y esperá la respuesta. |
| `Agent` / `subagent_type: X` | Delegar en el subagente `agente/agents/X.md`. Sin subagentes: seguí ese archivo vos. |
| `WebSearch` / `WebFetch` | Buscar y leer en la web. Sin web: decilo y no afirmes de memoria. |
| `Read` / `Write` / `Edit` / `Grep` / `Glob` | Leer, escribir y buscar archivos. |

## Reglas del repo

- Todo lo que producen las skills va a `temas/`, no al chat.
- `temas/*` está ignorado salvo `temas/ejemplo/`: los temas reales son del usuario.
- Los `profesor-*` de `agente/agents/` son personales y están ignorados.
- La config propia de cada agente (`.claude/`, `CLAUDE.md`, etc.) va a
  `.git/info/exclude`, nunca a `.gitignore`.
