from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Car, Booking, Brand
from .serializers import CarSerializer, BookingSerializer, BrandSerializer
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from booking.models import Booking, Car, Status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from .utils import send_booking_email

class BrandsViews(ModelViewSet):
    """
    Viewset for managing car brands.
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['brand_name']

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Success', BrandSerializer(many=True))
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CarListView(ModelViewSet):
    """
    Viewset for listing and retrieving cars.
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['status', 'car__car_brand__brand_name', 'car__car_model']

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Success', CarSerializer(many=True))
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class BrandListView(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer



class BookingCreateView(ModelViewSet):
    """
    Viewset for creating and managing bookings.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['status', 'car__car_brand__brand_name', 'car__car_model']



    @swagger_auto_schema(
        responses={
            200: openapi.Response('Success', BookingSerializer(many=True))
        }
    )

    def retrieve(self, request, pk=None):
        """Retrieve a single booking by ID with car details"""
        try:
            booking = self.get_object()
            serializer = self.get_serializer(booking)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        booking = serializer.save(user=self.request.user)
        # Mark the car as inactive
        car = booking.car
        car.status = "inactive"
        car.save()
        
         # Send booking confirmation email
        subject = f"Booking Confirmed"
        message = (
            f"Hi {booking.customer_first_name},\n\n"
            f"Your booking of car by 'Rent a Ride' from {booking.from_date} to {booking.to_date} "
            f"has been confirmed. Total Price: Rs. {booking.total_price}.\n\n"
            "Thank you for using our Car Rental Service!"
        )
        send_booking_email(subject, message, booking.email) # Send email to the user
    


    def update(self, request, pk=None):
        """Update booking status and update car status accordingly"""
        from .models import Status
        try:
            booking = self.get_object()
            new_status = request.data.get("status")

            if new_status not in dict(Status.choices).keys():
                return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

            booking.status = new_status
            booking.save()

            # If booking is canceled, set car as active
            if new_status == Status.CANCELLED:
                booking.car.status = "active"
                booking.car.save()

            return Response(
                {"message": "Booking status updated successfully", "status": booking.status},
                status=status.HTTP_200_OK
            )
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)





class CancelBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        booking_id = request.data.get("booking_id")

        if not booking_id:
            return Response({"error": "Booking ID is required"}, status=400)

        booking = get_object_or_404(Booking, id=booking_id, user=request.user)

        # Reverse the booking and car status
        booking.status = Status.CANCELLED
        booking.car.status = "active"

        booking.save()
        booking.car.save()
        
        # Send cancellation email
        subject = f"Booking Cancelled"
        message = (
            f"Hi {booking.customer_first_name},\n\n"
            f"Your booking of car by 'Rent a Ride' has been successfully cancelled.\n\n"
            "We hope to serve you again!"
        )
        send_booking_email(subject, message, booking.email)

        return Response({"message": "Booking cancelled and car status updated successfully"}, status=200)