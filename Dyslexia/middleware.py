from django.http import HttpResponse
from django.core.cache import cache

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        key = f"rl_{ip}"

        requests = cache.get(key, 0)

        if requests > 100:
            return HttpResponse("Too many requests", status=429)

        cache.set(key, requests + 1, timeout=60)

        return self.get_response(request)