# Footage y encuadre

## Dónde buscar

1. **Wikimedia Commons**, con `scripts/buscar_commons.py`. Para un hecho reciente suele haber una categoría (`--categoria "2026 Panama earthquake"`). La ficha trae licencia, fecha de toma, autor y descripción con el lugar: es lo que va a `source.md`.
   - Las fotos y videos de organismos de EE. UU. (Ejército, Departamento de Estado, USGS) suelen ser de dominio público.
   - `--filtro "collapsed|damage"` y `--licencia "Public domain|CC BY"` ayudan a quedarse con planos de daños y licencias claras.
2. **DVIDS** (archivo audiovisual del Departamento de Defensa de EE. UU.): material en bruto de dominio público, pero pide crear una cuenta para descargar. Eso lo hace la persona.
3. **Compilados de medios en YouTube** (con `yt-dlp`): útiles para el momento exacto del hecho, pero con derechos y con planos de origen dudoso. Si el usuario decide usarlos para uso interno, registralo y no publiques el repo con esos archivos.

No hay footage de dominio público del momento de un sismo: lo que hay es el después. Decilo al proponer el guion.

## Qué plano sí y qué plano no

- **Lugar y fecha verificados o no va.** Un derrumbe acreditado «Video: X» sin lugar ni fecha fue un P0: no se sabía si era de ese sismo ni de ese país, y como iba después de «Epicentro: Azuero» se leía como si fuera de ahí.
- **Que el plano no diga más que la nota.** Un colapso total cuando la nota habla de daños parciales exagera.
- **Cuidado con el protagonista.** Si la única presencia humana son rescatistas de un país extranjero y la nota no habla de ayuda internacional, el short sugiere una historia que la nota no tiene. Preferí planos de daños, sin personas identificables.
- **Un plano casi quieto se lee como foto.** Medí el movimiento si importa (`select='gte(scene,0)'`, cambio medio por cuadro); si es casi cero, que el crédito no prometa «video».

## Recetas de encuadre (ffmpeg)

Recorte corto, sin audio, H.264:
```bash
ffmpeg -ss 18.4 -t 1.8 -i fuente.webm -an -c:v libx264 -crf 19 -preset slow -pix_fmt yuv420p -movflags +faststart media/plano.mp4
```

Plano horizontal completo para meter entre barras (recorta las marcas de agua del canal en los bordes):
```bash
ffmpeg -ss 6 -t 2.6 -i compilado.mp4 -an -vf "crop=1600:900:60:180,scale=1080:608:flags=lanczos" -c:v libx264 -crf 18 -pix_fmt yuv420p media/plano-ancho.mp4
```
En la composición: el video en un contenedor de 1080×608 centrado, fondo con diseño (no negro liso: parece una falla), titular y fecha arriba, crédito abajo. Si animás la escala, hacelo sobre un contenedor interno, nunca sobre el `<video>`.

Plano vertical que ya viene 9:16: usalo a pantalla completa.

Fotos de Commons: pedí la miniatura de 2000 px (`iiurlwidth=2000`) y no la original de 6000 px.

## Mapas

- Si el círculo o la máscara del mapa puede mostrar el borde de la imagen durante un zoom, calculá la escala mínima para que el borde quede tapado, o fundí el mapa en el color de fondo con un degradé. Extender la imagen con un color plano deja una costura visible.
- El epicentro va como «Epicentro aproximado» y con la fuente (USGS).
