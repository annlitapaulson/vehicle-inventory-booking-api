
from datetime import date
from rest_framework import serializers
from .models import Vehicle, Booking


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'id',
            'vehicle',
            'customer_name',
            'customer_phone',
            'start_date',
            'end_date',
            'total_amount',
        ]
        read_only_fields = ['id', 'total_amount']

    def validate_customer_phone(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError(
                "Phone number must contain exactly 10 digits."
            )
        return value

    def validate_start_date(self, value):
        if value < date.today():
            raise serializers.ValidationError(
                "Start date cannot be in the past."
            )
        return value

    def validate(self, data):
        start_date = data.get(
            'start_date',
            getattr(self.instance, 'start_date', None)
        )
        end_date = data.get(
            'end_date',
            getattr(self.instance, 'end_date', None)
        )
        vehicle = data.get(
            'vehicle',
            getattr(self.instance, 'vehicle', None)
        )

        if start_date and end_date and end_date <= start_date:
            raise serializers.ValidationError({
                'end_date': 'End date must be after start date.'
            })

        if vehicle and start_date and end_date:
            overlapping_bookings = Booking.objects.filter(
                vehicle=vehicle,
                start_date__lt=end_date,
                end_date__gt=start_date,
            )

            if self.instance:
                overlapping_bookings = overlapping_bookings.exclude(
                    pk=self.instance.pk
                )

            if overlapping_bookings.exists():
                raise serializers.ValidationError(
                    "This vehicle is already booked for overlapping dates."
                )

        return data
