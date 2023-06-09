from django.urls import path
# from django.views.decorators.csrf import csrf_exempt
from .views import UserProfilePictureView, UserDocumentView
# from allauth.socialaccount.providers.google import views as google_view
# from allauth.account.views import LoginView

urlpatterns = [
    path('user/<int:pk>/image/', UserProfilePictureView.as_view(), name='user-image-upload'),
    path('user/<int:pk>/documents/', UserDocumentView.as_view(), name='documents-upload'),
    # path('user/auth/login/', google_view.oauth2_login, name='google_login'),
    # path('user/login/', csrf_exempt(UserLogin.as_view()), name='account_login'),
    # path('user', csrf_exempt(UserView.as_view()), name='account_user'),
    # path('user/signup/', csrf_exempt(UserSignUp.as_view()), name='account_signup'),
    # path('user/logout/', csrf_exempt(UserLogOut.as_view()), name='account_logout'),
    # path('user/auth/login/callback/', google_callback, name='google_callback'),
]
