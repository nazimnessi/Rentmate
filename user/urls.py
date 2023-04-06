from django.urls import path
from .views import UserProfilePictureView, UserDocumentView

urlpatterns = [
    path('user/<int:pk>/image/', UserProfilePictureView.as_view(), name='user-image-upload'),
    path('user/<int:pk>/documents/', UserDocumentView.as_view(), name='documents-upload'),
]
