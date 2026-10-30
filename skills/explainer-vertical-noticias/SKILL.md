---
name: explainer-vertical-noticias
description: Hacer o mejorar un explainer vertical de noticias (short, reel o TikTok de unos 20 s en 9:16) a partir de una nota, con HyperFrames y una persona en los puntos de control. Cubre guion por tiempos, footage con licencia verificada, storyboard, render, control de nivel medido (ritmo, quietud, tiempo de lectura y sonido audible en celular), crítica adversarial con otro agente y versiones numeradas. Usalo siempre que alguien pida convertir una nota en un video vertical, «un short de esta noticia», «un explainer de 20 segundos», mejorar o «llevar al nivel» un short de noticias existente, sumarle footage o música, o revisar uno antes de publicarlo, aunque no nombre HyperFrames.
---

# Explainer vertical de noticias

Un short de noticias de 20 s hecho por un agente, con una persona que dirige en tres puntos de control. Sale de iterar dos explainers en el taller de Media Party Buenos Aires 2026: el terremoto de Panamá (de la v4 a la v12) y el choque de trenes en Urda, Toledo (de la v1 a la v7).

La idea de fondo: el agente hace muchas vueltas de producción y de control; la persona pone el criterio editorial y decide en los puntos de control. Ningún control automático ve errores de contenido, así que siempre hay crítica adversarial sobre el render.

## Antes de empezar

- Cargá el skill `hyperframes` (es la entrada obligatoria para componer y renderizar) y leé `hyperframes-core` antes de escribir HTML.
- Si el proyecto fija una versión de HyperFrames, usá esa.
- Si el proyecto tiene lineamientos propios (estilo, referencias de nivel), leelos antes del guion.

## El flujo

### 0. La nota y los datos (`source.md`)

Armá o actualizá `source.md` en la carpeta del ejemplo: la nota con link, fecha y autor; las citas textuales de cada dato que va a ir en pantalla (copiadas del HTML de la página, no parafraseadas); los datos oficiales; las diferencias entre fuentes. Es contra lo que el crítico compara cada cifra, así que tiene que existir antes del guion.

Mirá la fecha: si el balance es de hace días, el short tiene que decir de cuándo es («Sinaproc, segundo informe (10/10)»). Proyectar un balance viejo sin fecha hace mentir al gancho.

- **Los datos cambian mientras trabajás.** Un balance se actualiza por hora y el informe oficial puede llegar al día siguiente (en el choque de trenes, el primer informe del organismo investigador corrigió la velocidad y dos horarios después de la v7). Rechequeá cada cifra antes de cada render; si cambió, va en una versión nueva y las anteriores quedan con los datos que tenían.
- **Verificá la firma.** El autor está en `<meta name="author">` o en la firma visible; el JSON-LD a veces pone el crédito de la foto como autor.
- **Las estimaciones van atribuidas** («≈ 200 km/h · estimación del ministro»), y si después hay una fuente mejor, se reemplaza.
- **Conceptos distintos no se mezclan** aunque tengan la misma unidad: el tope del reglamento (40 km/h) no es la máxima del tramo (80 km/h).

### A. Guion por tiempos (punto de control A)

Proponé una tabla `t · qué se ve · texto` y esperá el ok antes de escribir código. Reglas que salen de las críticas:

- **Una sola idea.** En la v5 entraron nueve datos en 20 s y no se entendía ninguno. Fecha, magnitud o hecho central, lugar y un bloque de consecuencias alcanza.
- **Buscá el dato que hace la historia.** A veces es un contraste: «El reglamento pedía 40 km/h; el AVE iba a unos 200» dice más que la regla sola.
- **El gancho tiene el dato y la fecha**, entero desde el primer cuadro. Sin texto, el primer medio segundo de un footage puede leerse como otra cosa.
- **Tiempo de lectura:** cada texto dura al menos 0,5 s + 0,3 s por palabra. Unas 50 palabras en total para 20 s.
- **Nada de unidades mezcladas en un mismo gráfico** («viviendas afectadas», «residencias», «con daños parciales» no se suman ni se comparan), y no inventes totales que la nota no da.
- **Seguí el énfasis de la nota:** si la nota destaca una provincia, el gráfico no la puede dejar última.
- **Cierre con una pregunta que la nota contesta**, y el link a la nota.

### Footage y material

Leé `references/footage.md`. En resumen: buscá con `scripts/buscar_commons.py` (licencia, fecha, lugar y autor en la ficha), usá solo planos que muestren lo que la nota dice, y si un plano no tiene lugar y fecha verificados, no va. Si el usuario decide usar material con derechos para uso interno, registralo así en `source.md` y avisá antes de publicar el repo. Pedí permiso antes de cada descarga, con archivo, fuente y tamaño.

### B. Storyboard (punto de control B)

Escribí la composición, corré `hyperframes check` (0 errores) y sacá un cuadro por escena con `hyperframes snapshot --at …`. Guardalos como `storyboard/vN-escena-K.png` (nunca borres la carpeta: tiene los de versiones anteriores). Mostralos, señalá vos mismo lo que ves flojo y esperá las notas. El formato de nota del taller es `t=… · dónde · problema → cambio`.

Reglas de composición que salieron de iterar:

- **Las cifras entran con su valor final** (escala u opacidad). Un contador que cuenta muestra cifras falsas casi todo el tiempo, y una captura puede salir con cualquiera.
- **Un dato nacional no va sobre la foto de un lugar concreto**: se lee como si fuera de ese lugar.
- **El ritmo está adentro de cada escena** (algo entra, se dibuja o se mueve cada 1 o 2 s), no en sumar cortes y datos.
- **Gráficos que se dibujan al ritmo de la frase**, con un sistema fijo: fondo liso, raya de acento, título con unidad, fuente abajo.
- **Créditos y fuentes de 30 px o más, dentro de la zona segura** (texto entre 260 px desde arriba, 480 px desde abajo y 180 px desde la derecha).
- **Un plano horizontal en vertical va completo, entre barras diseñadas**, no recortado a 9:16 (se pixela) ni sobre un relleno desenfocado (se ve barato). Recortá las marcas de agua del canal.
- **Lo decorativo no parece documento:** un trazo de sismógrafo o un gráfico ilustrativo sin ejes ni valores, y sin el aspecto de un registro real.
- **Un esquema es esquema o es figurativo, no a mitad de camino.** En el choque de trenes funcionó como diagrama de señalización: una línea para la vía, trazos con número para los trenes, la señal en rojo. Rotulá solo lo que dan las notas y marcalo («Esquema · posiciones aproximadas»).
- **El movimiento tiene que ser coherente con los datos.** Un tren que acelera justo antes del choque contradice los registros de velocidad; un vehículo que salta de posición entre escenas, también.
- **No cortes entre dos fondos iguales.** Si el dato siguiente vive en el mismo esquema, metelo adentro (una señal de velocidad en la vía) en lugar de pasar a una placa aparte.
- **La zona segura depende de dónde se publica.** Para redes, todo adentro; si no va a redes, fuentes y créditos pueden ir al pie del cuadro.

### Sonido

Leé `references/sonido.md`. El audio real del hecho va adelante, la música baja debajo de ese audio, todo normalizado a −14 LUFS. Los graves por debajo de unos 110 Hz no se oyen en un celular: medí la banda audible, no solo la sonoridad.

Si un medio publicó audios del hecho (grabaciones, llamadas), pedí el ok antes de bajarlos, acreditalos y poné la transcripción en pantalla con quién habla. Alargá la escena lo que haga falta para que entre la frase entera: el clip puede pasar de 20 s.

### C. Render, nivel y crítica (punto de control C)

1. Renderizá a `<ejemplo>-vN.mp4` con un número nuevo. El render guarda los cuadros en disco (de 1,2 a 1,4 GB para 20 s): si falla por espacio, usá `--workers 1`, que codifica mientras captura.
2. Corré el control de nivel:
   ```bash
   python3 scripts/medir_nivel.py <ejemplo>-vN.mp4 --html index.html
   ```
   Falla si algo queda quieto más de 2 s, si un texto dura menos que su tiempo de lectura, si la sonoridad está lejos de −14 LUFS o si hay segundos sin señal audible en celular. Informa los cortes pero no los exige: en la v5 del terremoto, perseguir cortes empeoró la legibilidad.
3. Lanzá la crítica adversarial con un agente nuevo que no armó el video. El brief está en `references/critico.md`.
4. Mostrá al usuario el video, las métricas contra la versión anterior y los P0, P1 y P2 del crítico. Los P0 se arreglan; los P1 y P2 los decide la persona.

### Versiones y registro

- Cada cambio es una versión nueva: `index.html` es la copia de trabajo; la anterior va a `versiones/index-vN.html` (con las rutas `../`), el render a `<ejemplo>-vN.mp4` y una línea a «Versiones» en `source.md`. Nunca pises un `-vN` ni dejes un MP4 sin número.
- En `source.md` registrá también: el material nuevo con licencia, fecha, lugar y URL; lo que encontró cada crítica; y las lecciones. Es lo que permite que otra persona o agente retome el trabajo sin repetir errores.
- No commitees ni pushees sin el ok del usuario. No subas cachés (`.media/`).

## Lo que este skill no hace

No reemplaza el criterio editorial: la persona decide qué se cuenta, aprueba el guion y los P1. Tampoco verifica la nota de origen; verifica que el video diga lo mismo que la nota.
