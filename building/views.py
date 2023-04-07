from rest_framework import generics, permissions
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Building, Documents, Room
from .serializer import (BuildingDocumentSerializer, BuildingSerializer,
                         BuildingProfilePictureSerializer, RoomDocumentSerializer, RoomSerializer)


class BuildingProfilePictureView(generics.UpdateAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingProfilePictureSerializer
    parser_classes = (FileUploadParser,)
    # permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        building = self.get_object()
        building.photo = request.data['file']
        building.save()
        serializer = self.get_serializer(building)
        return Response(serializer.data)


class BuildingDocumentView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        building = Building.objects.get(pk=kwargs.get('pk'))
        serializer = BuildingDocumentSerializer(data=request.data)

        if serializer.is_valid():
            for document in request.FILES.getlist('documents'):
                file_obj = Documents(file=document, name=document.name)
                file_obj.save()
                building.documents.add(file_obj)
            building_serializer = BuildingSerializer(building)
            return Response(building_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomDocumentView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        room = Room.objects.get(pk=kwargs.get('pk'))
        serializer = RoomDocumentSerializer(data=request.data)

        if serializer.is_valid():
            for document in request.FILES.getlist('documents'):
                file_obj = Documents(file=document, name=document.name)
                file_obj.save()
                room.additional_photo.add(file_obj)
            room_serializer = RoomSerializer(room)
            return Response(room_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
