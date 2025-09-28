# Django-Middleware-0x03/chats/middleware.py
import logging
from datetime import datetime
from pathlib import Path

# place requests.log at project root (Django-Middleware-0x03/requests.log)
LOG_FILE = Path(__file__).resolve().parents[2] / "requests.log"

logger = logging.getLogger("request_logger")
if not logger.handlers:
    fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
    fh.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(fh)
    logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    """
    Basic middleware that logs every request with timestamp, user, and path.
    Must implement __init__ and __call__ to pass the checks.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # if request.user is missing (e.g. during startup), handle gracefully
        user = "Anonymous"
        try:
            if hasattr(request, "user") and request.user.is_authenticated:
                # prefer email or username if available
                user = getattr(request.user, "email", None) or getattr(request.user, "username", None) or str(request.user)
        except Exception:
            user = "Anonymous"

        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        return self.get_response(request)
