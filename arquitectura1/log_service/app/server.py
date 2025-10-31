import grpc
from concurrent import futures
from arquitectura1.proto import urlhit_pb2, urlhit_pb2_grpc
from .storage import save_url_hit

DEFAULT_GRPC_ADDRESS = "127.0.0.1:50051" # ruta por defecto del servidor gRPC
# to-do: cambiar a .env


# se define una clase que implementa el servicio logService que es para mostrar los hits de las urls
# la clase es para extender la clase generada por grpc a partir del .proto
class LogService(urlhit_pb2_grpc.LogServiceServicer):
    # implementacion del metodo RegisterHit
    def RegisterHit(self, request, context):
        # request: UrlHit
        print(f"url hit recibido: {request.hash} -> {request.long_url}") # esto es para logger
        
        # guardar el hit en la base de datos
        save_url_hit(request.hash, request.long_url, request.timestamp)
        return urlhit_pb2.Ack(status="ok")

# funcion para iniciar el servidor gRPC
def serve(address: str = DEFAULT_GRPC_ADDRESS):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4)) # 4 hilos como workers
    urlhit_pb2_grpc.add_LogServiceServicer_to_server(LogService(), server) # se agrega el servicio al servidor
    
    
    server.add_insecure_port(address) # se agrega el puerto al servidor por insecure port
    server.start()
    
    
    print(f" logger: gRPC server escuchando en {address}")
    server.wait_for_termination()
