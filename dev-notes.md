### notas

- la base de datos va a ser en SQLite
- se necesita un venv de python y solo se usa 1 para ambas arquitecturas.

### crear venv de python

- Crear entorno virtual
```shell
python -m venv .venv
```

- Activar venv (windows)
```shell
.venv\Scripts\activate
```

Linux
```shell
source .venv/bin/activate
```

- instalar dependencias
```shell
pip install litestar grpcio grpcio-tools pybase62 sqlite-utils
```


- guardar en requirements.txt
```shell
pip freeze > requirements.txt
```

- o instalar del archivo requirements
```shell
pip install -r requirements.txt
```


### compilar el .proto de arqui1 
```shell
python -m grpc_tools.protoc -I=proto --python_out=proto --grpc_python_out=proto proto/urlhit.proto
```