from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import action
from app.OTP.serializer import OTPSerializer
from app.OTP.otp_util import OTPUtil
from app.OTP.cache_util import CacheUtil


class OTPViewSet(viewsets.ViewSet):

    parser_classes = [JSONParser]
    otp_util = OTPUtil()
    cache_util = CacheUtil()


    def create(self, request):
        """
        This is the public api method for creating an OTP
        It takes in a JSON containing phone number
        """
        serializer = OTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            generated_otp = self.otp_util.generate_otp()
            request_phone_number = serializer.validated_data.get('phone_number')
            retrieved_otp = self.cache_util.save_otp_to_cache(phone_number=request_phone_number, otp = generated_otp, timeout=10)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'otp_code' : retrieved_otp}, status=status.HTTP_200_OK)   

    @action(detail=False, methods=['post'])
    def verify_otp(self, request):
        """
        This is the public api for verifying an OTP
        It takes in a JSON containing phone number and OTP_code
        """
        serializer = OTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request_otp_code = serializer.validated_data.get('otp_code')
        request_phone_number = serializer.validated_data.get('phone_number')
        if not request_otp_code:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            retrieved_otp = self.cache_util.retrieve_otp_from_cache(phone_number=request_phone_number)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            if retrieved_otp == request_otp_code:
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)