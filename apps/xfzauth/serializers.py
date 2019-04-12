#encoding:utf-8
from rest_framework import serializers
from .models import User

class authorSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid','telephone','username','email','is_staff','is_active')

