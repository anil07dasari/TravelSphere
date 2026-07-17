from rest_framework import serializers
from .models import Car, Booking, Brand


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'



class CarSerializer(serializers.ModelSerializer):
    car_brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())  # ✅ Include full brand details

    class Meta:
        model = Car
        fields = '__all__'  # ✅ Now includes car_brand details

    def to_representation(self, instance):
        """Customize output to show full brand details."""
        representation = super().to_representation(instance)
        representation['car_brand'] = BrandSerializer(instance.car_brand).data  # ✅ Full details in response
        return representation    




# class ListCarSerializer(serializers.ModelSerializer):
#     car_brand = BrandSerializer()  # ✅ Include full brand details

#     class Meta:
#         model = Car
#         fields = '__all__'  # ✅ Now includes car_brand details




class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    car_details = CarSerializer(source="car", read_only=True)
    class Meta:
        model = Booking
        fields = [
            "id",
            "user",  # Optional: Exclude this if you don't want it in the response
            "customer_first_name",
            "customer_last_name",
            "address",
            "cnic",
            "contact_number",
            "email",
            "car",
            "from_date",
            "to_date",
            "status",
            "car_details",
            'total_price'
        ]
        read_only_fields = ["status", "user"]  # Prevent user and status from being updated manually


