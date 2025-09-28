# chats/middleware.py
import logging
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

# Configure logging to requests.log
logging.basicConfig(
    filename="requests.log",
    level=logging.INFO,
    format="%(message)s"
)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Restrict access outside 6AM–9PM
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden("Access to chats is restricted during these hours.")
        return self.get_response(request)


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.user_requests = {}

    def __call__(self, request):
        if request.method == "POST" and "/messages" in request.path:
            ip = self.get_client_ip(request)
            now = datetime.now()

            if ip not in self.user_requests:
                self.user_requests[ip] = []

            # Filter timestamps within last 1 minute
            self.user_requests[ip] = [
                ts for ts in self.user_requests[ip] if now - ts < timedelta(minutes=1)
            ]

            if len(self.user_requests[ip]) >= 5:
                return HttpResponseForbidden("Rate limit exceeded. Try again later.")

            self.user_requests[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Example: only admins or moderators can access /admin/ or /moderate/
        restricted_paths = ["/admin/", "/moderate/"]
        if any(request.path.startswith(path) for path in restricted_paths):
            if not request.user.is_authenticated or request.user.role not in ["admin", "moderator"]:
                return HttpResponseForbidden("You do not have permission to access this resource.")
        return self.get_response(request)
