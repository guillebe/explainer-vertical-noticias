# Sonido para celular

## La idea

- **El audio real del hecho va adelante** (un set de TV en vivo cuando empieza a temblar dice más que cualquier música).
- **La música va debajo**, más baja en los momentos con audio real, con fade al final. Instrumental, sin letra, y de tono sobrio: una cortina de «alerta urgente» empuja a la alarma si la nota no lo justifica.
- **Una sola pista mezclada** (`<audio id="banda">` con `data-start="0"`), con los videos en `muted`. Es determinista y fácil de versionar: `media/banda-sonora-vN.m4a`.
- **Efectos** (golpes en cada cifra): opcionales. En el terremoto se probaron y se sacaron.

## Lo que no se oye

Los graves por debajo de unos 110 Hz no salen por los parlantes de un celular ni de una laptop. Un «rumor» de diseño sonoro o un golpe de 50 Hz miden bien en LUFS y no se escuchan. Siempre medí la banda audible:
```bash
ffmpeg -i video.mp4 -vn -af "highpass=f=200,volumedetect" -f null -
```
`scripts/medir_nivel.py` lo hace segundo a segundo y marca los segundos mudos.

## Receta de mezcla (ffmpeg)

Ejemplo para un video de 20 s: audio real del gancho (0 a 2,6 s) + música desde el segundo 6 del tema, baja durante el gancho y a pleno después, con fade final. Para otra duración, cambiá `-t 20`, `atrim=0:20` y el inicio del fade:
```bash
ffmpeg -i audio-real.wav -ss 6.0 -t 20 -i musica.m4a -filter_complex \
"[0]afade=t=out:st=2.2:d=0.4[s];\
[1]aresample=48000,volume='if(lt(t,2.2),0.25,if(lt(t,2.6),0.25+(t-2.2)/0.4*0.75,1))':eval=frame,afade=t=out:st=18.4:d=1.6[m];\
[s][m]amix=inputs=2:normalize=0,apad,atrim=0:20,loudnorm=I=-14:TP=-1.5:LRA=11,volume=2.6dB,alimiter=limit=0.84:level=false[o]" \
-map "[o]" -ar 48000 -ac 2 -c:a aac -b:a 192k media/banda-sonora-vN.m4a
```
`loudnorm` en una pasada suele quedar unos 2,5 dB abajo de −14 cuando hay silencios: por eso el `volume` y el limitador al final. Verificá con `ebur128=peak=true` (objetivo: I ≈ −14 LUFS, pico ≤ −1 dBFS).

Para sumar otro momento con audio real (una voz a los 8 s, otra a los 13 s), **no uses `adelay` después de `loudnorm`**: corre las marcas de tiempo en lugar de agregar silencio, y la voz queda al principio. Concatená silencio explícito delante de cada voz y volvé a 48 kHz después de cada `loudnorm`:
```bash
ffmpeg -i voz.m4a -filter_complex \
"anullsrc=r=48000:cl=stereo,atrim=0:8.0[sil];\
[0]loudnorm=I=-16,aresample=48000,aformat=channel_layouts=stereo[v];\
[sil][v]concat=n=2:v=0:a=1[o]" -map "[o]" media/voz-en-8s.wav
```
Después mezclá cada pista con `amix=normalize=0` y bajá la música mientras suenan las voces (en el choque de trenes, al 28 %). Medí al final que la banda dure lo que el video.

Si el comando se arma con muchas entradas, armá la lista de argumentos en Python (`subprocess.run([...])`): en zsh, una variable con varios `-i` no se separa en palabras.

## Música

- La del usuario primero (por ejemplo, generada con Suno). Copiala a `media/` y acreditála en `source.md`.
- Si no hay: el catálogo de HeyGen con `media-use` (necesita la CLI de `heygen`), o una librería libre de regalías como Pixabay Music (verificá la licencia de cada tema).
- Antes de mezclar, mirá la forma de onda (`showwavespic`) y la energía por segundo para elegir el tramo, del largo del video, que calza con su arco; no el principio por defecto.
- Medí la energía audible por segundo (filtrada por encima de 200 Hz), no la sonoridad total: un tema puede tener el pico donde no lo oís en un celular. Hacé coincidir el pico con el momento fuerte del video y la bajada con el balance o el cierre.
