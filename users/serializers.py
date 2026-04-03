from rest_framework import serializers
from .models import Role,User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password', 'confirm_password', 'role', 'is_active']

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if not password or not confirm_password:
            raise serializers.ValidationError("Password and confirm password are required")

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")

        validate_password(password)

        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')

        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user
    
class CustomTokenSerializer(TokenObtainPairSerializer):
    username_field = 'email'

class UserRetrieveUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password', 'role', 'is_active']
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            validate_password(password)
            instance.set_password(password)

        instance.save()
        return instance