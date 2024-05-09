from django.db import models

class Vendor(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the vendor")
    contact_details = models.TextField(help_text="Contact information of the vendor")
    address = models.TextField(help_text="Physical address of the vendor")
    vendor_code = models.CharField(max_length=50, unique=True, help_text="A unique identifier for the vendor")
    on_time_delivery_rate = models.FloatField(default=0, help_text="Percentage of on-time deliveries")
    quality_rating_avg = models.FloatField(default=0, help_text="Average rating of quality based on purchase orders")
    average_response_time = models.FloatField(default=0, help_text="Average time taken to acknowledge purchase orders")
    fulfillment_rate = models.FloatField(default=0, help_text="Percentage of purchase orders fulfilled successfully")

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(help_text="Date when the order was placed")
    delivery_date = models.DateTimeField(help_text="Expected or actual delivery date of the order")
    items = models.JSONField(help_text="Details of items ordered")
    quantity = models.IntegerField(help_text="Total quantity of items in the PO")
    status = models.CharField(max_length=50, help_text="Current status of the PO (e.g., pending, completed, canceled)")
    quality_rating = models.FloatField(null=True, help_text="Rating given to the vendor for this PO (nullable)")
    issue_date = models.DateTimeField(help_text="Timestamp when the PO was issued to the vendor")
    acknowledgment_date = models.DateTimeField(null=True, help_text="Timestamp when the vendor acknowledged the PO")

    def __str__(self):
        return self.po_number
