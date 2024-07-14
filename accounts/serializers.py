from djoser.serializers import UserCreateSerializer
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *

from django.contrib.auth import get_user_model
User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('__all__')


class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class EmplyeeCodeSerializer(ModelSerializer):
    class Meta:
        model = EmplyeeCode
        fields = '__all__'


        
class UpdateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('last_name', 'department', 'password')

    def validate_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect")
        return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.department = validated_data.get('department', instance.department)
        
        instance.save()
        return instance
