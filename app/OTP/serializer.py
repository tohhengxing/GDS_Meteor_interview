from tempfile import TemporaryFile
from rest_framework import serializers


class OTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    otp_code = serializers.CharField(required=False)


    def validate_phone_number(self, value):
        error_message = "default error"
        try:
            if not value.isdigit():
                error_message = "phone number is not all numbers"
                raise Exception
            if len(value) != 8:
                error_message = "phone number is not correct length"
                raise Exception
        except Exception as e:
            raise serializers.ValidationError(error_message)
        else:
            return value

    def validate_otp_code(self, value):
        try:
            int(value)
        except Exception as e:
            raise serializers.ValidationError("otp cannot parse into number")
        else:
            return value




