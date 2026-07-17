from django.urls import path
from .views import CreateCarBookingCheckoutSession, stripe_webhook
from . import views

urlpatterns = [
    path('create-car-checkout-session/', CreateCarBookingCheckoutSession.as_view(), name='create-car-checkout'),
    path('stripe-webhook/', stripe_webhook, name='stripe-webhook'),
]