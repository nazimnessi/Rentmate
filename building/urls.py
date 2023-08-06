from django.urls import path
from .views import BuildingDocumentView, BuildingProfilePictureView, PropertyAPI, RoomDocumentView

urlpatterns = [
    path('building/<int:pk>/image/', BuildingProfilePictureView.as_view(), name='building-image-upload'),
    path('building/<int:pk>/documents/', BuildingDocumentView.as_view(), name='buillding-documents-upload'),
    path('room/<int:pk>/images/', RoomDocumentView.as_view(), name='room-images-upload'),
    path('property-download/', PropertyAPI.as_view({"get": "download"}), name='property-download'),
]
