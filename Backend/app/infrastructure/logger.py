import logging
import json
import os
from datetime import datetime

LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "logs"))
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "audit.log")

logger = logging.getLogger("audit")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(LOG_FILE)
    fmt = logging.Formatter("%(message)s")
    fh.setFormatter(fmt)
    logger.addHandler(fh)


def audit_log(actor: str, action: str, vm_id: str, provider: str, success: bool, details=None):
    payload = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "actor": actor,
        "action": action,
        "vm_id": vm_id,
        "provider": provider,
        "success": success,
        "details": details,
    }
    # evitar credenciales sensibles: nunca registramos 'params' completos ni secretos
    logger.info(json.dumps(payload))
