# serializers.py

from rest_framework import serializers
from .models import Vendor
from .models import PurchaseOrder



class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ('on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        # Specify datetime format for fields
        extra_kwargs = {
            'order_date': {'format': '%Y-%m-%dT%H:%M:%S'},
            'delivery_date': {'format': '%Y-%m-%dT%H:%M:%S'},
            'issue_date': {'format': '%Y-%m-%dT%H:%M:%S'},
            'acknowledgment_date': {'format': '%Y-%m-%dT%H:%M:%S'},
        }

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
