from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import urllib3
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

def google_callback(request):
    params = urllib3.parse.urlencode(request.GET)
    print(params)
    return redirect(f'http://localhost:3000/buildings/{params}')


from allauth.account.views import LoginView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.contrib.auth import authenticate, login

@method_decorator(csrf_exempt, name='dispatch')
def CustomLoginView(request):
    if request.method == 'POST':
        print(1111111111111111111111111)
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'email': email})
        else:
            return JsonResponse({'success': False})

