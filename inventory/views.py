from decimal import Decimal

from django.db import transaction
from rest_framework import generics
from rest_framework.exceptions import ValidationError

from .models import Vehicle, Booking
from .serializers import VehicleSerializer, BookingSerializer
class VehicleListCreateView(generics.ListCreateAPIView):
    serializer_class = VehicleSerializer

    def get_queryset(self):
        queryset = Vehicle.objects.all()

        brand = self.request.query_params.get('brand')
        fuel_type = self.request.query_params.get('fuel_type')
        is_available = self.request.query_params.get('is_available')

        if brand:
            queryset = queryset.filter(brand__iexact=brand)

        if fuel_type:
            queryset = queryset.filter(fuel_type__iexact=fuel_type)

        if is_available is not None:
            if is_available.lower() == 'true':
                queryset = queryset.filter(is_available=True)
            elif is_available.lower() == 'false':
                queryset = queryset.filter(is_available=False)

        return queryset

class VehicleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        vehicle_id = serializer.validated_data['vehicle'].pk
        vehicle = Vehicle.objects.select_for_update().get(pk=vehicle_id)

        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']

        overlapping_bookings = Booking.objects.filter(
            vehicle=vehicle,
            start_date__lt=end_date,
            end_date__gt=start_date,
        )

        if overlapping_bookings.exists():
            raise ValidationError(
                "This vehicle is already booked for those dates."
            )

        days = (end_date - start_date).days
        total_amount = Decimal(days) * vehicle.price_per_day

        serializer.save(total_amount=total_amount)

        vehicle.is_available = False
        vehicle.save(update_fields=['is_available'])


class BookingDetailView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
