# Discusión de Arquitectura y Trade-offs

## Arquitectura 1 (HTTP 302 + gRPC + Analítica)

En la arquitectura 1 el shortener redirige con un 302, lo que obliga al navegador a consultar siempre al servidor.
Esto tiene ventajas y desventajas, por un lado permite contar cada acceso y aplicar controles como listas negras o expiraciones, pero también hace que todo pase por el servidor, aumentando la latencia y la carga.
En el contexto de la USM, esto tendría sentido si se quisiera priorizar tener analítica precisa de las visitas más que optimizar rendimiento.

El **servicio de logs** con gRPC también ayuda a separar responsabilidades, porque el shortener sólo envía los eventos y otro proceso se encarga de guardarlos. Eso da flexibilidad si se quisiera más adelante integrar dashboards o estadísticas.
El problema es que agrega complejidad, es otro proceso que hay que mantener, más comunicación, y posibles fallos si el log no responde.
Para esta tarea es manejable debido a que es un entorno pequeño y de pruebas, pero en producción habría que monitorear bien los errores y asegurarse de no perder hits (un hit lo consideramos en nuestras implementaciones como una visita a una URL corta, es decir, cada vez que alguien hace un GET sobre una dirección acortada).

SQLite se mantuvo como base de datos por simplicidad y que nos permite utilizar/controlar de manera mas sencilla los id autoincremental, ya que no se busca rendimiento masivo. En un entorno real se usaría algo más robusto.

Los certificados HTTPS se generaron de forma local, lo que cumple el requisito de conexión segura (aunque el navegador va a mostrar advertencias).


## Arquitectura 2 (HTTP 301 + Rate Limiter + Cache)

Esta versión apunta más al rendimiento que a la analítica.
La redirección 301 permite que los navegadores y caches intermedios guarden la equivalencia, lo que reduce carga en el servidor.
La desventaja es que se pierde visibilidad de cuántos accesos reales hubo, porque muchas redirecciones ya no llegan al backend.

El **rate limiter** cumple con la táctica de controlar el arribo de eventos: evita que un cliente sature el servicio enviando muchas peticiones seguidas.
Es simple, pero hay que calibrarlo bien, porque si se deja un límite muy bajo puede bloquear usuarios legítimos.
En un despliegue real se podría ajustar según tipo de cliente o endpoint.

Nosotros tenemos por defecto 3 peticiones en una ventana de tiempo durante 15 segundos, pero esto es solamente para probarlo de manera rápida durante el desarrollo y para que sea más sencillo para el ayudante revisor sin tener que modificar estos parámetros en el archivo `config.py` de la arquitectura.
Sin embargo, esta cantidad de peticiones y la ventana de tiempo dependen completamente del contexto donde se despliegue el servicio.
Por ejemplo, en un entorno de producción o con uso público se dejaría un margen mucho más alto, o se diferenciaría por tipo de endpoint (más estricto para el POST /shorten y más laxo para el GET /{hash}).
La idea es demostrar la táctica de controlar el arribo de eventos, no dejar este valor definitivo.

El uso de cache en memoria mejora el tiempo de respuesta, porque evita acceder al disco para URLs que se consultan seguido.
Sin embargo, el cache es local, así que si se reinicia el proceso se pierde, y no sirve si se tienen varios nodos en paralelo.
En el contexto de la USM, esta arquitectura sería más conveniente si el objetivo es tener un servicio más rápido y con menor mantenimiento, por ejemplo, en escenarios donde se priorice disponibilidad sobre analítica detallada o se atienda un alto volumen de accesos de estudiantes o usuarios externos.

## Comparación general

La arquitectura 1 da más control y trazabilidad, mientras que la arquitectura 2 es más ligera y rápida.
La elección depende de qué se priorice: si la analítica detallada y el registro de eventos, o el rendimiento y la eficiencia.
Si la USM pidiera estadísticas precisas de uso, la primera tendría más sentido.
Si lo que se busca es rapidez y bajo costo de mantenimiento, la segunda sería la opción más práctica.


## BONUS
Para asegurar la unicidad de los id de los registros se pueden utilizar identificadores con offsets (rangos de IDs) unicos por nodos, es decir: 

`id = offset_inicial + offset_nodo + (contador_local * salto)`

Donde salto = 10^n y n es el número de dígitos que corresponden al offset del nodo.

Esta solución tiene la ventaja de no requerir comunicación entre los nodos, con la desventaja de que limita el número máximo de nodos que soporta el sistema (10^n nodos).
