from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import PurchaseOrder, Vendor
from django.db import models

@receiver(post_save, sender=PurchaseOrder)
@receiver(post_delete, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, **kwargs):
    vendor = instance.vendor

    # Calculate on-time delivery rate
    completed_orders = vendor.purchaseorder_set.filter(status='completed')
    total_completed_orders = completed_orders.count()
    on_time_orders = completed_orders.filter(delivery_date__lte=models.F('acknowledgment_date'))
    on_time_delivery_rate = (on_time_orders.count() / total_completed_orders) * 100 if total_completed_orders > 0 else 0

    # Calculate quality rating average
    quality_rating_avg = vendor.purchaseorder_set.filter(quality_rating__isnull=False).aggregate(avg_rating=models.Avg('quality_rating'))['avg_rating'] or 0

    # Calculate average response time
    response_times = vendor.purchaseorder_set.filter(acknowledgment_date__isnull=False).annotate(
        response_time=models.ExpressionWrapper(models.F('acknowledgment_date') - models.F('issue_date'), output_field=models.DurationField())
    )
    average_response_time = response_times.aggregate(avg_response=models.Avg('response_time'))['avg_response'] or 0

    # Calculate fulfillment rate
    fulfilled_orders = vendor.purchaseorder_set.filter(status='completed', quality_rating__isnull=False)
    fulfillment_rate = (fulfilled_orders.count() / total_completed_orders) * 100 if total_completed_orders > 0 else 0

    # Update vendor performance metrics
    vendor.on_time_delivery_rate = on_time_delivery_rate
    vendor.quality_rating_avg = quality_rating_avg
    vendor.average_response_time = average_response_time
    vendor.fulfillment_rate = fulfillment_rate
    vendor.save()
