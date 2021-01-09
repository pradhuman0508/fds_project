from rest_framework import serializers
from .models import Device





class DeviceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Device
        read_only_fields = ('qr_code_token',)

        fields = ('qr_code_token','serial_number','mac_address')
        extra_kwargs = {
            'serial_number': {'write_only': True},
            'mac_address': {'write_only': True},
        }

    def create(self,validated_data):
        device = Device(
            serial_number=validated_data['serial_number'],
            mac_address=validated_data['mac_address'],

        )
        device.save()
        return device


