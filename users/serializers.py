from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from django.forms import ValidationError
from django.contrib.auth.hashers import make_password

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    
    """Serializer class for user registration"""
    
    confirm_password = serializers.CharField(max_length=250, write_only=True, style={'input_type': 'password'})
    

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'confirm_password', 'first_name', 'last_name', 'date_joined', 'date_updated', 'is_staff', 'is_active', 'is_verified']
        extra_kwargs = {
            'password': {'write_only': True, 'style' : {'input_type': 'password'}},
            'date_joined': {'read_only': True},
            'date_updated': {'read_only': True},
            'is_verified': {'read_only': True},
            'is_active': {'read_only': True},
            'is_staff': {'read_only': True},
        }

    def validate(self, attrs):
        
        password = attrs.get('password')
        confirm_password = attrs.pop('confirm_password')

        if password != confirm_password:
            raise ValidationError(_("Passwords didn't match"))

        return attrs

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    
    """Serializer class for email verification of users"""

    token = serializers.CharField(trim_whitespace=True)
    
    class Meta:
        model = get_user_model()
        fields = ['token']


class SendEmailVerificationSerializer(serializers.Serializer):
    
    """Serializer class for sending email verification"""

    email = serializers.EmailField()


class SendPasswordResetEmailSerializer(serializers.Serializer):

    """Serializer class for sending password reset email"""

    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):

    """Serializer class for resetting password"""

    password = serializers.CharField(max_length=250, style={'input_type': 'password'})
    confirm_password = serializers.CharField(max_length=250, style={'input_type': 'password'})

    def validate(self, attrs, *args, **kwargs):

        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise ValidationError(_('Passwords did noy match'))

        print(attrs)

        return super().validate(attrs)



class AuthTokenSerializer(serializers.Serializer):
    
    """Serializer class for authenticating user"""

    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=8, write_only=True, style={'input_type':'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')


        user = authenticate(request=self.context.get('request'), username=email, password=password)

        print(user)

        if not user:
            msg = _('Validation failed, invalid credentials')
            raise ValidationError(message=msg, code='authentication')
        
        
        if not user.is_active:
            msg = _('User is blocked, please contact admin.')
            raise ValidationError(message=msg, code='not_active')


        if not user.is_verified:
            msg = _('Email is not verified, please verify your email.')
            raise ValidationError(message=msg, code='not_verified') 
        
        attrs['user'] = user

        return attrs


class TokenVerificationSerializer(serializers.Serializer):

    """Serializer class for token verification"""
    
    token = serializers.CharField(trim_whitespace=True)
