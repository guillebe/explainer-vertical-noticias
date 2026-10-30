# Footage y encuadre

## Dónde buscar

En este orden, de menos a más riesgo:

1. **Material propio o del medio** para el que se hace el video: fotos y videos con derechos claros.
2. **Wikimedia Commons**, con `scripts/buscar_commons.py`. Para un hecho reciente suele haber una categoría (`--categoria "2026 Panama earthquake"`). La ficha trae licencia, fecha de toma, autor y descripción con el lugar: es lo que va a `source.md`. `--filtro "collapsed|damage"` y `--licencia "Public domain|CC BY"` ayudan a quedarse con planos y licencias claras.
3. **Material oficial con licencia abierta:** organismos públicos, agencias de emergencia, servicios geológicos o meteorológicos. Revisá la licencia de cada uno: el dominio público de los organismos federales de EE. UU. no vale igual para los de otros países, y muchos piden crédito.
4. **Archivos audiovisuales públicos** (por ejemplo, DVIDS en EE. UU.): material en bruto, a veces con cuenta para descargar. La cuenta la crea la persona.
5. **Fotos de agencia** (EFE, Reuters, AP, Europa Press): tienen derechos. Solo con el ok de la persona, con el crédito completo en pantalla («Foto: agencia / autor · fecha») y registradas en `source.md` como de uso restringido.
6. **Compilados de medios en redes o YouTube** (con `yt-dlp`): útiles para el momento exacto del hecho, pero con derechos y con planos de origen dudoso. Solo para uso interno, registrado, y no se publica nada con esos archivos sin licencia.

**Ilustraciones y montajes de medios no son fotos del hecho.** Si el epígrafe dice «Imagen ilustrativa» o «Montaje», no van.

Si no hay material del momento exacto (en un sismo casi nunca lo hay: lo que hay es el después), decilo al proponer el guion y resolvelo con gráfico o esquema.

## Qué plano sí y qué plano no

- **Lugar y fecha verificados o no va.** Un derrumbe acreditado «Video: X» sin lugar ni fecha fue un P0: no se sabía si era de ese sismo ni de ese país, y como iba después de «Epicentro: Azuero» se leía como si fuera de ahí.
- **Que el plano no diga más que la fuente.** Un colapso total cuando la nota habla de daños parciales exagera.
- **Cuidado con el protagonista.** Si la única presencia humana son rescatistas de un país extranjero y la fuente no habla de ayuda internacional, el video sugiere una historia que la fuente no tiene. Preferí planos de daños, sin personas identificables.
- **Un plano casi quieto se lee como foto.** Medí el movimiento si importa (`select='gte(scene,0)'`, cambio medio por cuadro); si es casi cero, que el crédito no prometa «video».

## Recetas de encuadre (ffmpeg)

Recorte corto, sin audio, H.264:
```bash
ffmpeg -ss 18.4 -t 1.8 -i fuente.webm -an -c:v libx264 -crf 19 -preset slow -pix_fmt yuv420p -movflags +faststart media/plano.mp4
```

Plano horizontal completo para meter entre barras (recorta las marcas de agua del canal en los bordes):
```bash
ffmpeg -ss 6 -t 2.6 -i compilado.mp4 -an -vf "crop=1600:900:60:180,scale=720:405:flags=lanczos" -c:v libx264 -crf 18 -pix_fmt yuv420p media/plano-ancho.mp4
```
En la composición: el video en un contenedor de 720×405 centrado, fondo con diseño (no negro liso: parece una falla), titular y fecha arriba, crédito abajo. Si animás la escala, hacelo sobre un contenedor interno, nunca sobre el `<video>`.

Plano vertical que ya viene 9:16: usalo a pantalla completa.

Fotos de Commons: pedí una miniatura de unos 1500 px (`iiurlwidth=1500`), que alcanza para zoom en 720, y no la original de 6000 px.

## Mapas

- Si el círculo o la máscara del mapa puede mostrar el borde de la imagen durante un zoom, calculá la escala mínima para que el borde quede tapado, o fundí el mapa en el color de fondo con un degradé. Extender la imagen con un color plano deja una costura visible.
- Un punto en el mapa que no es exacto se rotula como aproximado («Epicentro aproximado») y lleva su fuente.
