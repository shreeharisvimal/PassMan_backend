from django.db import models
from user_management.models import User

class Password(models.Model):

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='passwords')
	app_name = models.CharField(max_length=255, null=False)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-id']

		
	def __str__(self):
        	return f"{self.app_name} - {self.user.credential}"
	

class BlackList(models.Model):

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='BlackList')
	password = models.ForeignKey(Password, on_delete=models.CASCADE, related_name='BlackList')
	UsedAt = models.DateTimeField(auto_now_add=True)
