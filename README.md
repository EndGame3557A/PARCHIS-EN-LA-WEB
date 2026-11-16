# Parchís

Versión web renovada del proyecto, con partidas en el mismo dispositivo, contra la computadora y salas privadas en línea. La interfaz y las fichas usan una identidad visual original y no dependen de escudos de equipos.

## Ejecutar en Windows

1. Instala Node.js 20 o posterior.
2. Desde esta carpeta, ejecuta `npm install`.
3. Ejecuta `npm start`.
4. Abre <http://localhost:3000>.

Para comprobar las reglas del juego, ejecuta `npm test`.

## Partidas en línea

El servidor acepta conexiones WebSocket y reparte los dados de manera autoritativa. Para que otras personas se unan, despliega este proyecto en un servicio que permita conexiones WebSocket y exponga la variable de entorno `PORT` (por ejemplo, una aplicación Node en Render, Fly.io o un VPS). Comparte el enlace de invitación que aparece en la sala.

Las salas y las partidas se guardan en memoria: si se reinicia el servidor, se pierden. Antes de un lanzamiento comercial habría que añadir persistencia, límites y protección contra abuso, monitorización y una política de privacidad adecuada.

## Reglas de esta versión

- **Clásico:** cuatro fichas por equipo, dobles para salir y recorrido completo.
- **La Previa:** una ficha por equipo, salida directa y cada dado mueve el doble; gana quien llegue primero.
- Al terminar, muestra el resumen de capturas y permite compartir el reto desde el menú de compartir del dispositivo o WhatsApp.
- En **Clásico**, se sale de casa con dobles y, si todas las fichas están en casa, hay tres intentos.
- En **Clásico** puedes sumar los dados o repartirlos entre dos fichas. En ambos formatos, los dobles permiten tirar otra vez.
- En **Clásico**, el tercer doble consecutivo lleva a casa la ficha más avanzada.
- Se requiere el número exacto para llegar a la meta.
- Las casillas seguras protegen; una ficha rival sola puede ser capturada en las demás casillas.

Las reglas se concentran en `public/game.js` para facilitar su prueba y evolución.
