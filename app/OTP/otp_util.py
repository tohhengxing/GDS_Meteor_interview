import random

TEMPLATE = "0123456789"
LENGTH = 6


class OTPUtil:

    def generate_otp(self) -> str:
        otp = ""
        for i in range(LENGTH):
            otp += TEMPLATE[random.randrange(len(TEMPLATE))]
        return otp