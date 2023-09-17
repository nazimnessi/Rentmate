from django.urls import path
# from django.views.decorators.csrf import csrf_exempt
from .views import IsUserLoginView, UserAuthenticateView, UserContactUsMail, UserLoginView, UserLogoutView, UserProfilePictureView, UserDocumentView
# from allauth.socialaccount.providers.google import views as google_view
# from allauth.account.views import LoginView

urlpatterns = [
    path('user/<int:pk>/image/', UserProfilePictureView.as_view(), name='user-image-upload'),
    path('user/<int:pk>/documents/', UserDocumentView.as_view(), name='documents-upload'),
    path('sentMail/', UserContactUsMail.as_view(), name='sent-contact-us-mail'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('isLogin/', IsUserLoginView.as_view(), name='isLogin'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('authenticate/', UserAuthenticateView.as_view(), name='authenticate'),
]
