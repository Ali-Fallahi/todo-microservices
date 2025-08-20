import logging
import time
import uuid

# یک لاگر جدید برای این ماژول ایجاد می‌کنیم
logger = logging.getLogger(__name__)


class StructuredLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # شروع زمان‌سنجی
        start_time = time.time()

        # ایجاد یک شناسه منحصر به فرد برای هر درخواست
        request_id = str(uuid.uuid4())

        # اجرای view و دریافت پاسخ
        response = self.get_response(request)

        # پایان زمان‌سنجی و محاسبه مدت زمان
        duration = time.time() - start_time

        try:
            # استخراج ID کاربر از توکن (اگر کاربر لاگین باشد)
            user_id = request.user.id if request.user.is_authenticated else None
        except AttributeError:
            user_id = None

        # ساخت دیکشنری لاگ ساختاریافته
        log_data = {
            "path": request.path,
            "method": request.method,
            "status_code": response.status_code,
            "duration_ms": int(duration * 1000),
            "request_id": request_id,
            "user_id": user_id,
            "remote_addr": request.META.get("REMOTE_ADDR"),
        }

        # ارسال لاگ با سطح اهمیت INFO
        logger.info("Request handled", extra={"structured_log": log_data})

        return response
