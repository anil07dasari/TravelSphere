from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password, CommonPasswordValidator, \
    UserAttributeSimilarityValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator


from rest_framework import serializers
from accounts.models import CustomUser



class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True) 
    password = serializers.CharField(write_only=True, min_length=8, required=False)

    class Meta:
        model = CustomUser
        fields = ["id", "email", "first_name", "last_name", "phone_number", "address", "image", 'password', 'roles']

    def to_representation(self, instance):
        data = super(ProfileSerializer, self).to_representation(instance)
        data.pop("password", None) 
        return data
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    password = serializers.CharField(min_length=8)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'first_name', 'last_name','phone_number']

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        data.pop('password', None)
        data['message'] = "successful"
        return data


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    image = serializers.ImageField(required=False)  # Add image field

    class Meta:
        model = CustomUser
        fields = ['email', 'cnic', 'phone_number', 'address', 'password', 'first_name', 'last_name', 'roles', 'image']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        image = validated_data.pop('image', None)  # Extract image
        user = CustomUser.objects.create_user(**validated_data)
        
        if image:
            user.image = image
            user.save()
            
        return user


# Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")
        
        # Return the user object with the role
        return {
            "user": user,
            "role": user.roles,  # Extract user role from model
        }

class ResetPasswordEmail(serializers.Serializer):
    email = serializers.EmailField(required=True)

class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, min_length=8)
    uuid = serializers.CharField(required=True)
    expiry = serializers.FloatField(required=False)

    def validate_new_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        if CommonPasswordValidator().validate(value):
            raise serializers.ValidationError('This password is too common.')
        if UserAttributeSimilarityValidator().validate(value):
            raise serializers.ValidationError('This password is too similar to personal information.')
        return value