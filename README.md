# Tarea-2-INF326
Grupo 7

Integrantes:

    Javier Hormaechea: 
    Benjamin Camus ROL: 202173072-9

### Requerimientos

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

1. Ejecutar shortener
```shell
python -m arquitectura1.shortener.main
```

2. Ejecutar el LogService
```shell
python -m arquitectura1.log_service.main
```

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

