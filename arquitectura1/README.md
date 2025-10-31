
comando compilar proto
```shell
cd arquitectura1/proto
python -m grpc_tools.protoc --python_out=. --grpc_python_out=. --proto_path=. urlhit.proto
```