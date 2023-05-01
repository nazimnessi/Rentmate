# from django.forms import ValidationError
from rest_framework import serializers
from .models import User, Documents
# from django.contrib.auth import authenticate, login


class UserProfilePictureSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = User
        fields = ['photo', 'name']


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'


class UserDocumentSerializer(serializers.Serializer):
    documents = serializers.ListField(child=serializers.FileField(), required=True)
    name = serializers.CharField()


# class UserLoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField()

#     def check_user(self, clean_data):
#         user = authenticate(email=clean_data['email'], password=clean_data['password'])
#         if not user:
#             raise ValidationError('user not Found')
#         return user


# class UserSignUpSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = '__all__'

#     def create(self, data):
#         # example data
#         # data = {
#         #     "email": "nazimck@gmail.com",
#         #     "password": "testuser",
#         #     "phone_number": "+918921666666",
#         #     "username": "username",
#         #     "aadhar": "1230987"
#         # }
#         print(data)
#         user = User.objects.create_user(**data)
#         user.save()
#         return user
