# import json
# from django.contrib.auth import login, logout
# from django.http import JsonResponse
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
# from allauth.account.views import LoginView
from rest_framework import generics
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
# from rest_framework.authentication import SessionAuthentication
from .models import User, Documents
from .serializer import UserProfilePictureSerializer, UserSerializer, UserDocumentSerializer
from django.contrib.auth import authenticate, login, logout
from google.oauth2 import id_token
from google.auth.transport import requests


class UserProfilePictureView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfilePictureSerializer
    parser_classes = (FileUploadParser,)
    permission_classes = (permissions.IsAuthenticated,)

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


class UserContactUsMail(APIView):

    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        from_email = request.data.get('from_email')
        subject = request.data.get('subject')
        message = request.data.get('message')

        if name and from_email and subject and message:
            html_message = render_to_string('contactUs.html', {
                'name': name,
                'subject': subject,
                'from_email': from_email,
                'message': message.replace('\\n', '<br>'),
            })

            send_mail(
                subject=subject,
                message="",
                from_email=from_email,
                recipient_list=[settings.EMAIL_HOST_USER],
                html_message=html_message
            )

            return Response({'message': 'Email sent successfully!'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Incomplete data'}, status=400)


# def google_callback(request):
#     params = urllib3.parse.urlencode(request.GET)
#     print(params)
#     return redirect(f'http://localhost:3000/buildings/{params}')


# class UserSignUp(APIView):
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request):
#         serializer = UserSignUpSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             user = serializer.create(data=request.data)
#             if user:
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            user = User.objects.get(email=request.data.get('email'))
        except Exception:
            return Response({"error": {"message": "Your username and password didn't match"}}, status=status.HTTP_401_UNAUTHORIZED)

        auth_user = authenticate(request, email=user.email, password=request.data.get('password'))
        if auth_user:
            login(request, auth_user)
            return Response({"status": True, "username": auth_user.username, "user_id": request.user.id}, status=status.HTTP_200_OK,)
        return Response({"error": {"message": "Your username and password didn't match. Please try again"}}, status=status.HTTP_401_UNAUTHORIZED)


class IsUserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            return Response({"status": True, "username": request.user.username, "user_id": request.user.id}, status=status.HTTP_200_OK)
        return Response({"status": False}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutView(APIView):

    def get(self, request):
        logout(request)
        return Response({"message": "User logged out successfully."}, status=status.HTTP_200_OK)


class UserAuthenticateView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        token = request.GET.get('token')
        user_info = id_token.verify_oauth2_token(token, requests.Request(), settings.CLIENT_ID)
        try:
            user = User.objects.get(email=user_info.get('email'))
        except Exception:
            return Response({"error": {"message": "User Does not have an account"}}, status=status.HTTP_401_UNAUTHORIZED)

        if user:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return Response({"status": True, "username": user.username, "user_id": user.id}, status=status.HTTP_200_OK,)
        return Response({"error": {"message": "account not found. try login manually or create a new account"}}, status=status.HTTP_401_UNAUTHORIZED)


# class UserView(APIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     authentication_classes = (SessionAuthentication,)

#     def get(self, request):
#         serializer = UserSerializer(request.user)
#         return Response({'user': serializer.data}, status=status.HTTP_200_OK)


# class UserLogOut(APIView):
#     permissions_classes = (permissions.IsAuthenticated,)
#     authentication_classes = (SessionAuthentication,)

#     def post(self, request):
#         logout(request)
#         return Response(status=status.HTTP_200_OK)
