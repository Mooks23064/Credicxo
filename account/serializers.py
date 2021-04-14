from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import update_last_login
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode as uid_decoder
from rest_auth.serializers import PasswordResetSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.settings import api_settings
from .forms import PasswordResetForm
from .models import User

# from rest_auth.serializers import PasswordResetSerializer


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

UserModel = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for User Registration
    """
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
            'first_name',
            'last_name',
            'user_role',
        )

    # Override default create function
    def create(self, validated_data):
        user_qs = User.objects.create_user(
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data.get('password', ''),
            user_role=validated_data.get('user_role', '')
        )

        user = authenticate(
            email=validated_data.get('email'),
            password=validated_data.get('password')
        )
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )

        data = {
            "id": user_qs.id,
            "email": validated_data.get('email'),
            "first_name": validated_data.get('first_name', ''),
            "last_name": validated_data.get('last_name', ''),
            "user_role": validated_data.get('user_role', ''),
            'token': jwt_token

        }
        return data


class UserLoginSerializer(serializers.ModelSerializer):
    """
    Serializer for User Login.
    """
    email = serializers.CharField(max_length=50)
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'token',
            'password',
        )

    @staticmethod
    def get_token(obj):
        try:
            payload = JWT_PAYLOAD_HANDLER(obj)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, obj)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return jwt_token


class CustomPasswordResetSerializer(PasswordResetSerializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    password_reset_form_class = PasswordResetForm


class CustomPasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm

    def custom_validation(self, attrs):
        pass

    def validate(self, attrs):
        self._errors = {}

        # Decode the uidb64 to uid to get User object
        try:
            params = self.context.get('request').query_params
            uid = force_text(uid_decoder(params.get('uid')))
            self.user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})

        self.custom_validation(attrs)
        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        if not default_token_generator.check_token(self.user, params.get('token')):
            raise ValidationError({'token': ['Invalid value']})

        return attrs

    def save(self):
        return self.set_password_form.save()
