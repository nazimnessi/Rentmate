# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from payment.models import Payment
import razorpay
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
from datetime import datetime

# Create your views here.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET)
)


class RazorPayView(APIView):
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        currency = "INR"
        amount = request.data.get("total_amount") * 100

        payment_instance = Payment.objects.get(pk=request.data.get("payment_id"))

        razorpay_order = razorpay_client.order.create(
            dict(amount=amount, currency=currency, payment_capture="0")
        )

        razorpay_order_id = razorpay_order["id"]
        callback_url = "api/v1/payments/payment_confirm"

        context = {}
        context["order_id"] = razorpay_order_id
        context["merchant_key"] = settings.RAZOR_KEY_ID
        context["amount"] = request.data.get("total_amount")
        context["currency"] = currency
        context["callback_url"] = callback_url
        context["username"] = payment_instance.payer.username
        context["email"] = payment_instance.payer.email
        context["phone_number"] = payment_instance.payer.phone_number

        return Response(context)


class CallbackView(APIView):
    """
    APIView for Verifying Razorpay Order.
    :return: Success and failure response messages
    """

    @staticmethod
    def post(request, *args, **kwargs):

        response = {
            "razorpay_payment_id": request.data.get("razorpay_payment_id"),
            "razorpay_order_id": request.data.get("razorpay_order_id"),
            "razorpay_signature": request.data.get("razorpay_signature"),
        }

        """
            if razorpay_signature is present in the request
            it will try to verify
            else throw error_reason
        """
        if "razorpay_signature" in response:

            # Verifying Payment Signature
            data = razorpay_client.utility.verify_payment_signature(response)

            # if we get here True signature
            if data:
                Payment.objects.filter(id__in=request.data.get("payment_ids")).update(
                    status="Paid",
                    transaction_id=request.data.get("razorpay_payment_id"),
                    transaction_date=datetime.now(),
                )

                return Response({"status": "Payment Done"}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"status": "Signature Mismatch!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Handling failed payments
        else:
            error_code = response["error[code]"]
            error_description = response["error[description]"]
            error_source = response["error[source]"]
            error_reason = response["error[reason]"]

            error_status = {
                "error_code": error_code,
                "error_description": error_description,
                "error_source": error_source,
                "error_reason": error_reason,
            }

            return Response(
                {"error_data": error_status}, status=status.HTTP_401_UNAUTHORIZED
            )
