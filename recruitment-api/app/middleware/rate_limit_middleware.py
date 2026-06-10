import time
from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_limit: int = 60, window_seconds: int = 60):
        super().__init__(app)
        self.requests_limit = requests_limit
        self.window_seconds = window_seconds
        # Store request timestamps for each client IP address
        self.client_records = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()

        # Remove old timestamps that fall outside the rolling time window
        active_requests = [
            timestamp for timestamp in self.client_records[client_ip]
            if current_time - timestamp < self.window_seconds
        ]
        self.client_records[client_ip] = active_requests

        # Check if the rate limit threshold has been exceeded
        if len(active_requests) >= self.requests_limit:
            return Response(
                content='{"detail": "Too many requests. Please try again later."}',
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                media_type="application/json"
            )

        # Register the current request timestamp
        self.client_records[client_ip].append(current_time)
        
        response = await call_next(request)
        return response