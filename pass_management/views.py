from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .Password_Manage import PasswordManagement
from .serializers import PasswordSerializer
from .models import Password

class PasswordCreateApi(APIView):
	
	permission_classes = [IsAuthenticated]

	def post(self, request):
		special_char = request.data.get('special_character', False)
		pass_length = request.data.get('length', 10)
		pass_content = request.data.get('content', None)

		try:
			pass_length = int(pass_length)
		except ValueError:
			return Response({'error': 'Invalid password length.'}, status=status.HTTP_400_BAD_REQUEST)

		Pass = PasswordManagement(special_char, pass_length, pass_content)
		NewUserPassword = Pass.CreatePassword()
		return Response(data={'password': NewUserPassword}, status=status.HTTP_201_CREATED)


class PasswordApi(APIView):
	permission_classes = [IsAuthenticated]

	def save(self, request, password, app_name):
		"""
		Save the password in the database.
		"""
		try:
			try:
				OldPassword = Password.objects.get(user = request.user, app_name = app_name)
				OldPassword.password = password
				OldPassword.save()
			except Password.DoesNotExist:
				Password.objects.create(user=request.user, app_name=app_name, password=password)
			return Response(status=status.HTTP_201_CREATED)
		except Exception as e:
			print(f"The error {e}")
			return Response({'error': 'An error occurred while saving the password.'}, status=status.HTTP_400_BAD_REQUEST)

	def post(self, request):
		password = request.data.get('password')
		app_name = request.data.get('app_name')
		print(password)
		app_name = app_name.capitalize() if app_name else ''

		if not password or not app_name:
			return Response({'error': 'Password and app name are required.'}, status=status.HTTP_400_BAD_REQUEST)

		return self.save(request, password, app_name)

	def get(self, request):
		"""
		Retrieve the password from the database.
		"""
		passwords = Password.objects.filter(user=request.user)
		serializer = PasswordSerializer(passwords, many=True) 
		return Response(data={'passwords':serializer. data}, status=status.HTTP_200_OK)
	
	def delete(self, request, id):
		password = Password.objects.get(id=id)
		password.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
