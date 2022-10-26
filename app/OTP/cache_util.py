from django.core.cache import cache

class CacheUtil:

    def __init__(self):
        self.cache = cache

    def save_otp_to_cache(self, phone_number: str, otp: str, timeout: int) -> str:
        self.cache.set(key=phone_number, value=otp, timeout=timeout)
        return self.cache.get(key=phone_number)

    def retrieve_otp_from_cache(self, phone_number: str) -> str:
        return self.cache.get(key=phone_number)
