from django.urls import path

from payment.views import CallbackView, RazorPayView

urlpatterns = [
    path("order", RazorPayView.as_view(), name="payments"),
    path("payment_confirm", CallbackView.as_view(), name="payment_confirm"),
]
