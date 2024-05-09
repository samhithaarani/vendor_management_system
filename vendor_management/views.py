from rest_framework import generics
from .models import Vendor
from .serializers import VendorSerializer
from .models import PurchaseOrder
from rest_framework.response import Response
from .serializers import PurchaseOrderSerializer
from .serializers import VendorPerformanceSerializer

class VendorPerformanceView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class PurchaseOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class VendorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
# views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer
from django.utils import timezone

@api_view(['POST'])
def acknowledge_purchase_order(request, po_id):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response({"message": "Purchase Order does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()
        return Response({"message": "Purchase Order acknowledged successfully"}, status=status.HTTP_200_OK)

