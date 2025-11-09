# Tarea-2-INF326
Grupo 7

Integrantes:

    Javier Hormaechea: 202003017-0
    Benjamin Camus ROL: 202173072-9

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

#### Endpoints Arquitectura 1

- `POST https://127.0.0.1:8000/shorten`
  - Cuerpo JSON: `{"url": "<url_larga>"}`.
  - Respuesta: `{"short_url": "https://127.0.0.1:8000/<hash>"}`.
  - Errores comunes: `400` si falta el campo `url`.
- `GET https://127.0.0.1:8000/<hash>`
  - Redirección `302` a la URL original (cabecera `Location`).
  - Si el hash no existe, responde `404`.
  - Cada petición genera un evento gRPC `UrlHit` hacia el LogService con timestamp y URL.

### Ejecutar Arquitectura 2

1. Entrar a la carpeta de la arquitectura
```shell
cd arquitectura2
cd shortener
```

2. Generar los certificados
```shell
python -m arquitectura2.shortener.generate_certs
```

3. Ejecutar shortener
```shell
python -m arquitectura2.shortener.main
```

