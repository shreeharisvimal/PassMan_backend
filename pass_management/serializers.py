from rest_framework import serializers

from . import models
from rest_framework.response import Response
from rest_framework import permissions, status


class PasswordSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Password
		fields = '__all__'