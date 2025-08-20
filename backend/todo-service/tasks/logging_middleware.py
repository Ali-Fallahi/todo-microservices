import logging
import time
import uuid

logger = logging.getLogger(__name__)


class StructuredLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        request_id = str(uuid.uuid4())
        response = self.get_response(request)
        duration = time.time() - start_time

        # اینجا ID کاربر را از هدر می‌خوانیم
        user_id = request.headers.get("X-User-ID")

        log_data = {
            "path": request.path,
            "method": request.method,
            "status_code": response.status_code,
            "duration_ms": int(duration * 1000),
            "request_id": request_id,
            "user_id": user_id,
            "remote_addr": request.META.get("REMOTE_ADDR"),
        }
        logger.info("Request handled", extra={"structured_log": log_data})
        return response
