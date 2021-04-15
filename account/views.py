
from account.serializers import UserRegistrationSerializer, UserLoginSerializer
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_auth.views import PasswordResetView, GenericAPIView
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from django.utils.decorators import method_decorator

from .serializers import CustomPasswordResetSerializer, CustomPasswordResetConfirmSerializer
from django.views.decorators.debug import sensitive_post_parameters

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)
class UserRegistrationView(generics.CreateAPIView):
    """
    Custom User Registration View.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = (IsAuthenticated,)
    """
    Token validation on role based
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            if new_user:
                return Response(
                    data={
                        "data": new_user
                    }, status=status.HTTP_201_CREATED
                )
        return Response(
            data={
                "message": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST
        )



class UserLoginView(generics.GenericAPIView):
    """
    User Login View
    """

    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            email=request.data['email'],
            password=request.data['password']
        )
        if user is not None:
            return Response({
                "success": True,
                "data": self.serializer_class(instance=user).data})
        else:
            return Response({
                "success": False,
                "detail": _("You are not registered user call to 'Admin'.")
            })


class CustomPasswordResetView(PasswordResetView):
    """
    Custom View To Overwrite Default Password Reset Email Template
    """
    serializer_class = CustomPasswordResetSerializer


class CustomPasswordResetConfirmView(GenericAPIView):
    """
    Password reset e-mail link is confirmed, therefore
    this resets the user's password.
    Accepts the following POST parameters: token, uid,
        new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = CustomPasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    @sensitive_post_parameters_m

    def dispatch(self, *args, **kwargs):
        return super(CustomPasswordResetConfirmView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": _("Password has been reset with the new password.")}
        )
