# Explainer vertical de noticias

Una skill para agentes (Claude Code, Codex y otros) que convierte una nota en un explainer vertical de unos 20 s (9:16, 1080×1920) con [HyperFrames](https://github.com/heygen-com/hyperframes), con una persona que decide en tres puntos de control: guion, storyboard y render.

Salió del taller «Contando historias verticales con agentes», de Media Party Buenos Aires 2026.

## Instalar

```bash
npx skills add guillebe/explainer-vertical-noticias
```

Usa [skills](https://github.com/vercel-labs/skills), que la instala en los agentes que tengas. Para elegir uno: `-a claude-code` o `-a codex`.

A mano: copiá la carpeta `skills/explainer-vertical-noticias` a la carpeta de skills de tu agente (en Claude Code, `~/.claude/skills/`).

## Qué más hace falta

- [Node.js](https://nodejs.org) (trae `npx`) y [FFmpeg](https://ffmpeg.org).
- Las skills de HyperFrames: `npx hyperframes skills`.
- Python 3 para los scripts de control.
- Para revisar todo: `npx hyperframes doctor`.

## Qué trae

- `SKILL.md`: el flujo, de la nota al render, con las reglas que salieron de iterar.
- `references/`: el brief del crítico adversarial, cómo elegir footage y cómo mezclar sonido para celular.
- `scripts/medir_nivel.py`: mide ritmo, quietud, tiempo de lectura y sonido audible en celular.
- `scripts/buscar_commons.py`: busca imágenes y videos en Wikimedia Commons con licencia, fecha, lugar y autor.

## Para usarla

Pedile a tu agente, por ejemplo: «Hacé un explainer vertical de 20 s de esta nota: [link]. Idea en una frase: [tu frase]». La skill se carga sola.

Guillermo Bertossi · Luciano Pereira
