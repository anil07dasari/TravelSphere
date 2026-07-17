import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import RetrieveAPIView
from .serializers import PaymentSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from booking.models import *
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCarBookingCheckoutSession(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a Stripe checkout session for subscription",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["plan_id"],
            properties={
                "plan_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Subscription Plan ID"),
            },
        ),
        responses={200: openapi.Response("Successful", openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "sessionId": openapi.Schema(type=openapi.TYPE_STRING, description="Stripe Session ID"),
            },
        ))},
    )
    
    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            booking_id = request.data.get("booking_id")
            print("booking_id:", booking_id)  # <--- Add this
            booking = get_object_or_404(Booking, id=booking_id, user=user)

            # Calculate total price in cents for Stripe
            # unit_amount = int(booking.total_price * 100)
            pkr_price = booking.total_price  # e.g., PKR 9000

            # Hardcoded exchange rate
            usd_rate = 278.5

            # Convert PKR to USD
            usd_price = round(pkr_price / usd_rate, 2)  # e.g., ~$32.3

            # Stripe needs amount in cents
            unit_amount = int(usd_price * 100)


            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                customer_email=user.email,
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f"Car Booking - {booking.car.car_model}",
                        },
                        'unit_amount': unit_amount,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=settings.STRIPE_SUCCESS_URL + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=settings.STRIPE_CANCEL_URL,
                metadata={"booking_id": str(booking.id)}
            )
            return JsonResponse({'url': checkout_session.url})

        except Exception as e:
            print("Error creating Stripe session:", e)
            return Response({'error': str(e)}, status=500)




@swagger_auto_schema(
    method='post',
    operation_description="Stripe webhook for handling payment events",
    responses={200: openapi.Response("Webhook processed successfully")},
)

@csrf_exempt
@api_view(['POST'])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers.get("Stripe-Signature", "")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'error': str(e)}, status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        booking_id = session.get("metadata", {}).get("booking_id")
        if not booking_id:
            return JsonResponse({'error': 'Missing booking ID'}, status=400)

        
        try:
            booking = Booking.objects.get(id=booking_id)
            user = booking.user

            # Check if payment already exists
            payment_exists = Payment.objects.filter(stripe_checkout_id=session.id).exists()
            if payment_exists:
                return JsonResponse({'error': 'Duplicate payment detected'}, status=400)

            # Create the Payment entry after successful checkout
            Payment.objects.create(
                user=user,
                booking=booking,
                stripe_checkout_id=session.id,
                amount=booking.total_price,
                status="Paid"
            )
            # booking.status = Status.APPROVED
            booking.status = Status.PAID
            booking.save()

        except Booking.DoesNotExist:
            return JsonResponse({'error': 'Booking not found'}, status=404)

    return JsonResponse({'status': 'success'})
