from django.db import models
from user_management.models import User
from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings

class PasswordManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset()

	def get(self, *args, **kwargs):
		password_instance = super().get(*args, **kwargs)
		password_instance.password = password_instance.decrypt_password()
		return password_instance

	def filter(self, *args, **kwargs):
		password_instances = super().filter(*args, **kwargs)
		for password_instance in password_instances:
			password_instance.password = password_instance.decrypt_password()
		return password_instances

class Password(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='passwords')
	app_name = models.CharField(max_length=255, null=False)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)

	objects = PasswordManager()  

	class Meta:
		ordering = ['-id']

	def encrypt_password(self, raw_password):
		"""
		Encrypt the password using the secret key.
		"""
		key = settings.ENCRYPTION_KEY 
		fernet = Fernet(key)
		encrypted_password = fernet.encrypt(raw_password.encode())
		return encrypted_password.decode()

	def decrypt_password(self):
		"""
		Decrypt the password to retrieve the original form.
		"""
		key = settings.ENCRYPTION_KEY
		fernet = Fernet(key)
		decrypted_password = fernet.decrypt(self.password.encode())
		return decrypted_password.decode()

	def save(self, *args, **kwargs):
		if not self.pk or Password.objects.get(pk=self.pk).password != self.password:
			self.password = self.encrypt_password(self.password)
		super(Password, self).save(*args, **kwargs)

	def __str__(self):
		return f"{self.app_name} - {self.user.username}"



class BlackList(models.Model):

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='BlackList')
	password = models.ForeignKey(Password, on_delete=models.CASCADE, related_name='BlackList')
	UsedAt = models.DateTimeField(auto_now_add=True)
