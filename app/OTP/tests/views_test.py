from unittest.mock import patch
from django.test import override_settings
from rest_framework.test import APITestCase
from django.urls import reverse


@override_settings(CACHES={'default':{'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
@patch('app.OTP.views.OTPViewSet.otp_util')
@patch('app.OTP.views.OTPViewSet.cache_util')
class OTPViewTest(APITestCase):

    def test_create_otp_with_correct_inputs(self, mock_cache_util, mock_otp_util):
        # Arrange
        url = reverse('otp-list')
        mock_otp = '123456'
        data = {'phone_number' : '12345678'}
        mock_cache_util.save_otp_to_cache.return_value = mock_otp
        mock_otp_util.generate_otp.return_value = mock_otp
        # Act
        response = self.client.post(url, data, format='json')
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'otp_code': mock_otp})


    def test_create_otp_with_incorrect_inputs(self, mock_cache_util, mock_otp_util):
        # Arrange
        url = reverse('otp-list')
        data = {'phone_number' : 'this is incorrect'}
        # Act
        response = self.client.post(url, data, format='json')
        # Assert
        self.assertEqual(response.data.get('phone_number')[0], 'phone number is not all numbers')
        self.assertEqual(response.status_code, 400)

    def test_create_otp_but_exception_occurs(self, mock_cache_util, mock_otp_util):
        # Arrange
        url = reverse('otp-list')
        mock_otp = '123456'
        data = {'phone_number' : '12345678'}
        mock_cache_util.save_otp_to_cache.return_value = mock_otp
        mock_otp_util.generate_otp.return_value = mock_otp
        mock_cache_util.save_otp_to_cache.side_effect = Exception 
        # Act
        response = self.client.post(url, data, format='json')
        # Assert
        self.assertEqual(response.status_code, 400)