import random
import string
from .models import User
from datetime import datetime
from django.core.mail import send_mail
from rest_framework.views import APIView
from django.core.cache import cache
from rest_framework import permissions, status
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer



# Get the current date and time


class MyRefreshTokenObtainPairSerializer(TokenRefreshSerializer):
	def __init__(self, *args, **kwargs):
		request = kwargs.pop('request', None)
		super().__init__(*args, **kwargs)

class MyRefreshTokenObtainPairView(TokenRefreshView):
	serializer_class = MyRefreshTokenObtainPairSerializer



class TemporaryUserManagement:
	def __init__(self, cred) -> None:
		self.__TempUserId = None
		self.__Otp = None
		self.__credential = cred

	def __generate_temp_id(self):
		now = datetime.now()
		uniquetime = f'{now.day:02}{now.month:02}{now.hour:02}{now.minute:02}{now.second:02}{now.microsecond // 1000:03}'
		return uniquetime
	
	def __generate_otp(self):
		otp = random.randint(100000, 999999)
		return otp
	
	def create_temp_user(self):
		self.__TempUserId = self.__generate_temp_id()
		self.__Otp = self.__generate_otp()
		self.__send_otp_to_email()
		return self.__TempUserId, self.__Otp
	

	def __send_otp_to_email(self):
		subject = 'Your OTP Code for JustBook'
		message = f'Your OTP code is {self.__Otp}'
		from_email = 'noreplay@example.com' 
		try:
			send_mail(subject, message, from_email, [self.__credential])
			return True
		except Exception as e:
			print(str(e))
			return str(e)
	
	



class LoginApi(APIView):

	def post(self, request):
		try:
			credential = request.data.get('credential')
			if not credential:
				return Response({"error": "Credential is required"}, status=status.HTTP_400_BAD_REQUEST)
			
			user_management = TemporaryUserManagement(credential)
			user_id, otp = user_management.create_temp_user()

			cache.set(f"otp_{user_id}", otp, timeout=180)
			cache.set(f"credential_{user_id}", credential, timeout=180)

			return Response(data={"user_id": user_id}, status=status.HTTP_201_CREATED)
		
		except Exception as e:
			return Response({"error": "An error occurred {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		



class GetLoginOtp(APIView):
	
	def post(self, request):
		otp = request.data.get('otp')
		user_id = request.data.get('user_id')

		if not otp or not user_id:
			return Response({"error": "OTP and user_id are required"}, status=status.HTTP_400_BAD_REQUEST)
		cache_key = f"otp_{user_id}"
		otp_stored = cache.get(cache_key)
		print(otp_stored)
		print(otp)

		if int(otp_stored) and int(otp_stored) == int(otp):
			cache.delete(cache_key)
			credential = cache.get(f'credential_{user_id}')

			User.objects.get_or_create(credential=credential)
			user = User.objects.get(credential=credential)

			cache.delete(f'credential_{user_id}')

			token = user.tokens()
			data = {
				'access_token': token['AccessToken'],
				'refresh_token': token['RefreshToken'],
			}
			
			return Response(data=data, status=status.HTTP_200_OK)
		elif otp_stored is None:
			return Response({"error": "Invalid OTP"}, status=status.HTTP_403_FORBIDDEN)
		else:
			return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
		

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
