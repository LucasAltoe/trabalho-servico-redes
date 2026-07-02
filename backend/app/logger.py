import os
import time
import httpx

LOKI_URL = os.getenv("LOKI_URL", "http://loki:3100")


def enviar_log(mensagem: str, nivel: str = "info") -> None:
    payload = {
        "streams": [
            {
                "stream": {"service": "fastapi", "level": nivel},
                "values": [[str(time.time_ns()), mensagem]],
            }
        ]
    }
    try:
        httpx.post(f"{LOKI_URL}/loki/api/v1/push", json=payload, timeout=2.0)
    except Exception:
        pass
