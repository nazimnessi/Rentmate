from django.http import HttpResponse

from payment.models import Payment
from .utils import email_verification_token_generator
from rest_framework import generics
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.files.storage import FileSystemStorage
from rest_framework import status
from rest_framework import permissions
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import User, Documents
from .serializer import (
    UserProfilePictureSerializer,
    UserSerializer,
    UserDocumentSerializer,
)
from django.contrib.auth import authenticate, login, logout
from google.oauth2 import id_token
from google.auth.transport import requests
from django.core.mail import EmailMessage
from weasyprint import HTML


class UserProfilePictureView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfilePictureSerializer
    parser_classes = (FileUploadParser,)
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        user.photo = request.data["file"]
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class UserDocumentView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs.get("pk"))
        serializer = UserDocumentSerializer(data=request.data)

        if serializer.is_valid():
            for document in request.FILES.getlist("documents"):
                file_obj = Documents(file=document, name=document.name)
                file_obj.save()
                user.documents.add(file_obj)
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Invoice(APIView):
    permission_classes = [permissions.AllowAny]
    swagger_schema = None

    def get(self, request, *args, **kwargs):
        payment_id = kwargs.get("payment_id")
        payment_instance = Payment.objects.get(id=payment_id)

        invoice_data = {
            "id": payment_instance.id,
            "invoice_date": payment_instance.created_date.strftime("%Y-%m-%d"),
            "renter_username": payment_instance.payer.username,
            "renter_fullname": f"{payment_instance.payer.first_name} {payment_instance.payer.last_name}",
            "renter_full_address": f"{payment_instance.payer.address.address1}, {payment_instance.payer.address.address2}, {payment_instance.payer.address.city}, {payment_instance.payer.address.state}, {payment_instance.payer.address.postal_code}",
            "renter_phone_number": payment_instance.payer.phone_number,
            "owner_username": payment_instance.payee.username,
            "owner_fullname": f"{payment_instance.payee.first_name} {payment_instance.payee.last_name}",
            "owner_full_address": f"{payment_instance.payee.address.address1}, {payment_instance.payee.address.address2}, {payment_instance.payee.address.city}, {payment_instance.payee.address.state}, {payment_instance.payee.address.postal_code}",
            "owner_phone_number": payment_instance.payee.phone_number,
            "description": payment_instance.note,
            "category": payment_instance.payment_category,
            "status": payment_instance.status,
            "amount": payment_instance.amount,
        }
        html_string = render_to_string(
            "invoice.html",
            {"invoice_instance": invoice_data, "host": request.build_absolute_uri("/")},
        )
        html = HTML(string=html_string)
        name = f"Invoice_{invoice_data.get('invoice_date')}.pdf"
        html.write_pdf(target=f"/tmp/{name}")
        fs = FileSystemStorage("/tmp")
        with fs.open(name) as pdf:
            response = HttpResponse(pdf, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="{name}.pdf"'
            return response


class UserContactUsMail(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        name = request.data.get("name")
        from_email = request.data.get("from_email")
        subject = request.data.get("subject")
        message = request.data.get("message")

        if name and from_email and subject and message:
            html_message = render_to_string(
                "contactUs.html",
                {
                    "name": name,
                    "subject": subject,
                    "from_email": from_email,
                    "message": message.replace("\\n", "<br>"),
                },
            )

            send_mail(
                subject=subject,
                message="",
                from_email=from_email,
                recipient_list=[settings.EMAIL_HOST_USER],
                html_message=html_message,
            )

            return Response(
                {"message": "Email sent successfully!"}, status=status.HTTP_200_OK
            )
        else:
            return Response({"error": "Incomplete data"}, status=400)


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            user = User.objects.get(email=request.data.get("email"))
        except Exception:
            return Response(
                {"error": {"message": "Your username and password didn't match"}},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        auth_user = authenticate(
            request, email=user.email, password=request.data.get("password")
        )
        if auth_user:
            login(request, auth_user)
            return Response(
                {
                    "status": True,
                    "username": auth_user.username,
                    "user_id": request.user.id,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "error": {
                    "message": "Your username and password didn't match. Please try again"
                }
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )


class IsUserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            return Response(
                {
                    "status": True,
                    "username": request.user.username,
                    "user_id": request.user.id,
                },
                status=status.HTTP_200_OK,
            )
        return Response({"status": False}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutView(APIView):

    def get(self, request):
        logout(request)
        return Response(
            {"message": "User logged out successfully."}, status=status.HTTP_200_OK
        )


class UserAuthenticateView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        token = request.GET.get("token")
        user_info = id_token.verify_oauth2_token(
            token, requests.Request(), settings.CLIENT_ID
        )
        try:
            user = User.objects.get(email=user_info.get("email"))
        except Exception:
            return Response(
                {"error": {"message": "User Does not have an account"}},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if user:
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return Response(
                {
                    "status": True,
                    "username": user.username,
                    "user_id": user.id,
                    "email": user.email,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "error": {
                    "message": "account not found. try login manually or create a new account"
                }
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )


class SendVerificationEmail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        email = request.GET.get("email")

        if not email:
            return Response(
                {"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        # You can use Django's built-in User model or your custom User model.
        user = User.objects.filter(email=email).first()

        if not user:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Generate a verification token
        token = email_verification_token_generator.make_token(user)

        # Construct the verification link with the token
        verification_link = (
            f"http://localhost:3000/verify-email/?email={email}&token={token}"
        )

        email_message = render_to_string(
            "EmailVerificationMail.html",
            {
                "user_name": user.username,
                "website_name": "Rentmate",
                "verification_url": verification_link,
                "support_email_address": "http://localhost:3000/contact-us",
            },
        )

        # Send the email with the verification link
        subject = "Email Verification"
        message = email_message
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        email = EmailMessage(
            subject,
            message,
            from_email,
            recipient_list,
        )
        email.content_subtype = "html"

        try:
            email.send()
            return Response(
                {"message": "Verification email sent successfully."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VerifyEmail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        email = request.GET.get("email")
        token = request.GET.get("token")

        if not email or not token:
            return Response(
                {"error": "Email and token are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(email=email).first()

        if not user:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Verify the token
        if email_verification_token_generator.check_token(user, token):
            # Mark the email as verified (You can customize this logic)]
            user.is_verified_email = True
            user.save()
            return Response(
                {"message": "Email verified successfully."}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST
            )
