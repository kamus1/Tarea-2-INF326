import logging
from datetime import datetime, timezone

import grpc

from arquitectura1.proto import urlhit_pb2, urlhit_pb2_grpc

from .config import GRPC_ADDRESS

logger = logging.getLogger(__name__)

# cliente gRPC para enviar eventos UrlHit al LogService
def send_url_hit(hash_str: str, long_url: str):
    timestamp = datetime.now(timezone.utc).isoformat()  # timestamp
    logger.debug(
        "send_url_hit: preparando evento hash=%s long_url=%s ts=%s",
        hash_str,
        long_url,
        timestamp,
    )

    # envia un evento UrlHit a log service
    try:
        with grpc.insecure_channel(GRPC_ADDRESS) as channel:
            stub = urlhit_pb2_grpc.LogServiceStub(channel)

            # request
            request = urlhit_pb2.UrlHit(
                hash=hash_str,
                long_url=long_url,
                timestamp=timestamp,
            )
            response = stub.RegisterHit(request, timeout=2.0)  # timeout de 2 segundos
            logger.info(
                "send_url_hit: evento enviado hash=%s status=%s",
                hash_str,
                response.status,
            )
    except grpc.RpcError as error:
        logger.exception(
            "send_url_hit: error gRPC al registrar hash=%s: %s",
            hash_str,
            error,
        )
    except Exception:
        logger.exception("send_url_hit: error inesperado al notificar hash=%s", hash_str)
