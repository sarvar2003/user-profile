from django.urls import path

from . import views

urlpatterns = [
    path("", views.api_root, name="main"),
    path("all/", views.AllUsersView.as_view(), name="all-users"),
    path("register/", views.RegistrationView.as_view(), name="registration"),
    path(
        "user/<str:email>/", views.RetrieveUserAPIView.as_view(), name="retrieve-user"
    ),
    path(
        "user/update/<str:email>/",
        views.UpdateUserDetailsAPIView.as_view(),
        name="update-user",
    ),
    path("token/", views.AuthTokenAPIView.as_view(), name="token"),
    path("verify-token/", views.VerifyTokenAPIView.as_view(), name="verify-token"),
    path(
        "verify-email/<str:token>/",
        views.EmailVerificationView.as_view(),
        name="verify-email",
    ),
    path(
        "send-verification-email/",
        views.SendEmailVerificationView.as_view(),
        name="send-verification-email",
    ),
    path(
        "send-password-reset-link/",
        views.SendPasswordResetEmailAPIView.as_view(),
        name="send-password-reset-link",
    ),
    path(
        "reset-password/<str:token>/",
        views.PasswordResetAPIView.as_view(),
        name="reset-password",
    ),
]
