from django.urls import path
from .views import CustomLoginView, UserProfilePictureView, UserDocumentView, google_callback
from allauth.socialaccount.providers.google import views as google_view
from allauth.account.views import LoginView

urlpatterns = [
    path('user/<int:pk>/image/', UserProfilePictureView.as_view(), name='user-image-upload'),
    path('user/<int:pk>/documents/', UserDocumentView.as_view(), name='documents-upload'),
    path('user/auth/login/', google_view.oauth2_login, name='google_login'),
    path('login/', CustomLoginView, name='account_login'),
    # path('user/auth/login/callback/', google_callback, name='google_callback'),
]
