import grpc
from datetime import datetime, timezone
from arquitectura1.proto import urlhit_pb2, urlhit_pb2_grpc
from .config import GRPC_ADDRESS

# cliente gRPC para enviar eventos UrlHit al LogService
def send_url_hit(hash_str: str, long_url: str):
    timestamp = datetime.now(timezone.utc).isoformat() # timestamp

    # envia un evento UrlHit a log service
    with grpc.insecure_channel(GRPC_ADDRESS) as channel:
        stub = urlhit_pb2_grpc.LogServiceStub(channel)
        
        # request
        request = urlhit_pb2.UrlHit(
            hash=hash_str,
            long_url=long_url,
            timestamp=timestamp,
        )
        try:
            response = stub.RegisterHit(request, timeout=2.0) # timeout de 2 segundos
            print(f"shortener: evento enviado: {response.status}")
        except grpc.RpcError as e:
            print(f"shortener: error gRPC: {e}")
