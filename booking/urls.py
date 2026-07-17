from django.urls import path
from .views import (
    CarListView,
    BookingCreateView,
    BrandsViews,
    CancelBookingView,

)

urlpatterns = [
    path('cars/', CarListView.as_view({"get": "list", "post": "create"}), name='car-list'),
    path('brands/', BrandsViews.as_view({"get": "list", "post": "create"}), name='car-list'),
    path('cars/<int:pk>', CarListView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}), name='car-list'),
    path('booking/', BookingCreateView.as_view({"get": "list", "post": "create"}), name='booking-create'),
    path('booking/<int:pk>/', BookingCreateView.as_view({"put": "update", "delete": "destroy", "get" : "retrieve"}), name='booking-create'),
    path('brand/', BrandsViews.as_view({"get": "list" }), name="brand-list"),
    path('brand/<int:pk>/', BrandsViews.as_view({"get": "retrieve", }), name="brand-list"),
    path('cancel/booking/', CancelBookingView.as_view(), name='cancel_booking'),
]