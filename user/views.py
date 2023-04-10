from rest_framework import generics
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User, Documents
from .serializer import UserProfilePictureSerializer, UserSerializer, UserDocumentSerializer


class UserProfilePictureView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfilePictureSerializer
    parser_classes = (FileUploadParser,)
    # permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        user.photo = request.data['file']
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class UserDocumentView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs.get('pk'))
        serializer = UserDocumentSerializer(data=request.data)

        if serializer.is_valid():
            for document in request.FILES.getlist('documents'):
                file_obj = Documents(file=document, name=document.name)
                file_obj.save()
                user.documents.add(file_obj)
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
