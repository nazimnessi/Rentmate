from django.urls import path
from .views import (
    Invoice,
    IsUserLoginView,
    SendVerificationEmail,
    UserAuthenticateView,
    UserContactUsMail,
    UserLoginView,
    UserLogoutView,
    UserProfilePictureView,
    UserDocumentView,
    VerifyEmail,
)

urlpatterns = [
    path(
        "user/<int:pk>/image/",
        UserProfilePictureView.as_view(),
        name="user-image-upload",
    ),
    path(
        "user/<int:pk>/documents/", UserDocumentView.as_view(), name="documents-upload"
    ),
    path("sentMail/", UserContactUsMail.as_view(), name="sent-contact-us-mail"),
    path("invoice/<str:payment_id>", Invoice.as_view(), name="invoice"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("isLogin/", IsUserLoginView.as_view(), name="isLogin"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("authenticate/", UserAuthenticateView.as_view(), name="authenticate"),
    path(
        "send-verification-email/",
        SendVerificationEmail.as_view(),
        name="send-verification-email",
    ),
    path("verify-email/", VerifyEmail.as_view(), name="verify-email"),
]
