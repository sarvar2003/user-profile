from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from rest_framework import generics, permissions, status, views
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.settings import api_settings

from . import serializers, utils

# Create your views here.


@api_view(["GET", "HEAD"])
def api_root(request, format=None):
    return Response(
        {
            "register": reverse("registration", request=request, format=None),
            "all-users": reverse("all-users", request=request, format=None),
            "token": reverse("token", request=request, format=None),
            "verify-token": reverse("verify-token", request=request, format=None),
            "send-verification-email": reverse(
                "send-verification-email", request=request, format=None
            ),
            "send-password-reset-link": reverse(
                "send-password-reset-link", request=request, format=None
            ),
        }
    )


class AllUsersView(generics.ListAPIView):
    """API view for listing all the users"""

    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = get_user_model().objects.all()


class RegistrationView(generics.GenericAPIView):
    """API view responsible for user registration"""

    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):

        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        # Sending verification email
        user = get_user_model().objects.get(email=user_data["email"])

        token, created_at  = Token.objects.get_or_create(user=user)
        current_site_domain = get_current_site(request).domain
        relativeLink = reverse("verify-email", kwargs={"token": token})
        verification_link = "http://" + current_site_domain + relativeLink
        message = ". Use this link to verify your email. \n If you were not expecting account verification email, please ignore this message \n."
        email_body = "Hi " + user.first_name + message + verification_link
        data = {
            "email_body": email_body,
            "email_subject": "Verify you account",
            "to_email": [user.email],
        }

        utils.Mail.send_mail(data=data)

        return Response(
            {"status": _("Verify your email"), "user": user_data},
            status=status.HTTP_201_CREATED,
        )


class RetrieveUserAPIView(generics.RetrieveDestroyAPIView):
    """API view responsible for retrieving a user"""

    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_object(self):
        return get_user_model().objects.get(email=self.kwargs.get("email"))


class UpdateUserDetailsAPIView(generics.RetrieveUpdateAPIView):
    """API view responsible for updating user details"""

    serializer_class = serializers.UpdateUserDetailsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return get_user_model().objects.get(email=self.kwargs.get("email"))


class EmailVerificationView(views.APIView):
    """API view responsible for user email verification"""

    serializer_class = serializers.EmailVerificationSerializer
    permission_classes = (permissions.AllowAny,)

    def get(self, request, token):

        try:
            user_token = Token.objects.get(key=token)

            user = get_user_model().objects.get(id=user_token.user.id)

            if not user.is_verified:
                user.is_verified = True
                user.is_active = True
                user.save()

            return Response(
                {
                    "status": _("Email successfully verified"),
                    "user": {
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "is_verified": user.is_verified,
                    },
                },
                status=status.HTTP_200_OK,
            )

        except Token.DoesNotExist:
            return Response(
                {"status": _("Invalid Token")}, status=status.HTTP_400_BAD_REQUEST
            )


class SendEmailVerificationView(views.APIView):
    """API view responsible for sending email verification"""

    serializer_class = serializers.SendEmailVerificationSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")

        try:
            user = get_user_model().objects.get(email=email)

            token, created_at = Token.objects.get_or_create(user=user)
            current_site_domain = get_current_site(request).domain
            relativeLink = reverse("verify-email", kwargs={"token": token})
            verification_link = "http://" + current_site_domain + relativeLink
            message = ". Use this link to verify your email. \n If you were not expecting any email verification, please ignore this message. \n"
            email_body = "Hi " + user.first_name + message + verification_link
            data = {
                "email_subject": "Email Verification",
                "email_body": email_body,
                "to_email": [email],
            }

            utils.Mail.send_mail(data=data)

            return Response(
                {"status": _("Email verification sent successfully")},
                status=status.HTTP_200_OK,
            )

        except get_user_model().DoesNotExist:
            return Response(
                {"status": _("User with given email does not exist")},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SendPasswordResetEmailAPIView(views.APIView):
    """API view for sending password reset email"""

    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.SendPasswordResetEmailSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")

        try:
            user = get_user_model().objects.get(email=email)

            token, created_at = Token.objects.get_or_create(user=user)
            current_site_domain = get_current_site(request).domain
            relativeLink = reverse("reset-password", kwargs={"token": token})
            absolute_url = "http://" + current_site_domain + relativeLink
            message = ". Use this link to reset your password. \n"
            email_body = "Hi " + user.first_name + message + absolute_url + "\n"
            data = {
                "email_subject": "Reset Password",
                "email_body": email_body,
                "to_email": [email],
            }

            utils.Mail.send_mail(data=data)

            return Response(
                {"status": _("Reset email sent successfully")},
                status=status.HTTP_200_OK,
            )

        except get_user_model().DoesNotExist:
            return Response(
                {"status": _("User with given email does not exist")},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PasswordResetAPIView(views.APIView):
    """API view for resetting user password"""

    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.ResetPasswordSerializer

    def get(self, request, token):

        try:
            user_token = Token.objects.get(key=token)

            try:
                get_user_model().objects.get(id=user_token.user.id)

                return Response({"status": "valid"})

            except get_user_model().DoesNotExist:

                return Response(
                    {
                        "status": _(
                            "Invalid token, user no longer exists in our system, please contact customer support"
                        )
                    }
                )

        except Token.DoesNotExist:
            return Response(
                {"status": _("Invalid token, please try again")},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def post(self, request, token):

        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        new_password = serializer.data["confirm_password"]
        print(f"New password - {new_password}")

        user_token = Token.objects.get(key=token)

        user = get_user_model().objects.get(id=user_token.user.id)

        user.set_password(new_password)

        user.save()

        return Response(
            {"status": _("Password successfully reset")}, status=status.HTTP_200_OK
        )


class VerifyTokenAPIView(views.APIView):
    """API view responsible for verifying token"""

    serializer_class = serializers.TokenVerificationSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data["token"]

        try:
            user_token = Token.objects.get(key=token)
        except Token.DoesNotExist:
            return Response({"status": "Invalid Token"})

        user = get_user_model().objects.get(id=user_token.user.id)

        return Response(
            {
                "status": "Valid Token",
                "token": Token.objects.get(user=user).key,
                "user_id": user.pk,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "date_joined": {
                    "year": user.date_joined.year,
                    "month": user.date_joined.month,
                    "day": user.date_joined.day,
                    "time": user.date_joined.time().strftime("%H:%M:%S"),
                },
                "date_updated": {
                    "year": user.date_joined.year,
                    "month": user.date_joined.month,
                    "day": user.date_joined.day,
                    "time": user.date_joined.time().strftime("%H:%M:%S"),
                },
            }
        )


class AuthTokenAPIView(ObtainAuthToken):
    """API view responsible for obtaining authentication token"""

    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        print(request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created_at = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": str(token),
                "user_id": user.pk,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "date_joined": {
                    "year": user.date_joined.year,
                    "month": user.date_joined.month,
                    "day": user.date_joined.day,
                    "time": user.date_joined.time().strftime("%H:%M:%S"),
                },
                "date_updated": {
                    "year": user.date_joined.year,
                    "month": user.date_joined.month,
                    "day": user.date_joined.day,
                    "time": user.date_joined.time().strftime("%H:%M:%S"),
                },
            }
        )
