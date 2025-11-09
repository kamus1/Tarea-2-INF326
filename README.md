# Tarea-2-INF326
Grupo 7

Integrantes:

    Javier Hormaechea: 202003017-0
    Benjamin Camus ROL: 202173072-9


### Consideraciones
- Utilizamos SQLite para las bases de datos.
- Se puede configurar los parámetros de arquitectura 2 como el rate limiter en `arquitectura2\shortener\app\config.py`, por default rate limiter está en 3 peticiones cada 15 segundos (pero esto solamente para que sea mas fácil probarlo y no esperar demasiado tiempo del rate limiter).


### Requisitos

1. Estar en la ruta raíz del repositorio `Tarea-2-INF326`

2. Crear .venv de python 
```shell
python -m venv .venv
```

3. Activar .venv
```shell
.venv\Scripts\activate
```

4. Instalar dependencias
```shell
pip install -r requirements.txt
```

### Ejecutar Arquitectura 1

1. Generar (o regenerar) certificados TLS
```shell
python -m arquitectura1.shortener.generate_certs
```

2. Ejecutar shortener
```shell
python -m arquitectura1.shortener.main
```

3. Ejecutar el LogService
```shell
python -m arquitectura1.log_service.main
```

### Ejecutar Arquitectura 2

1. Generar (o regenerar) certificados TLS
```shell
python -m arquitectura2.shortener.generate_certs
```

2. Ejecutar shortener
```shell
python -m arquitectura2.shortener.main
```


#### Endpoints Arquitectura 1

- `POST https://127.0.0.1:8000/shorten`
  - Cuerpo JSON: `{"url": "<url_larga>"}`.
  - Respuesta: `{"short_url": "https://127.0.0.1:8000/<hash>"}`.
  - Errores: `400` si falta el campo `url`.
- `GET https://127.0.0.1:8000/<hash>`
  - Redirección `302` a la URL original (cabecera `Location`).
  - Si el hash no existe, responde `404`.
  - Cada petición genera un evento gRPC `UrlHit` hacia el LogService con timestamp y URL.


#### Endpoints Arquitectura 2

- `POST https://127.0.0.1:8001/shorten`
  - Cuerpo JSON: `{"url": "<url_larga>"}`.
  - Respuesta: `{"short_url": "https://127.0.0.1:8001/<hash>"}`.
  - Errores: `400` (payload inválido o sin `url`), `429` si se supera el rate limit.
- `GET https://127.0.0.1:8001/<hash>`
  - Redirección `301` a la URL original (cabecera `Location`), lo que permite al navegador cachear.
  - Caché en memoria evita golpear la base en hashes populares (ver logs “cache hit/miss”).
  - Si el hash no existe, responde `404`.
 


### Ejemplo de Caching y rate limiter.
En la siguiente imagen se muestran logs al realizar peticiones GET a la arquitectura 2.
- En este ejemplo tenemos rate limiter de 3 peticiones cada 15 segundos (a modo de pruebas).
- Si se realiza una cuarta petición en la ventana de tiempo de los 15 segundos, se respinde con `429 Too Many Requests`
- La primera vez que se consulta por una ruta se puede ver que hay un `cache miss` por lo que tiene que hacer una consulta a la base de datos.
- Las demás veces se logra un `cache hit` debido a que tiene la url acortada guardada en cache por lo que no realiza nuevas peticiones a DB.
<img width="1222" height="262" alt="image" src="https://github.com/user-attachments/assets/4a927a45-6e3a-47ba-9864-3dc827671243" />


