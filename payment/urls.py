from django.urls import path

from .views import HomePageView, stripe_config, create_checkout_session, SuccessView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('config/', stripe_config),
    path('create-checkout-session/', create_checkout_session),
    path('success/', SuccessView.as_view(), name='success')
]
