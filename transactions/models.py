from django.db import models


class Seller(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    place = models.CharField(max_length=100, blank=True)
    remarks = models.TextField(blank=True)
    gst_no = models.CharField(max_length=30, blank=True)
    phone_no = models.CharField(max_length=20, blank=True)
    email_id = models.EmailField(blank=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name


class Buyer(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    place = models.CharField(max_length=100, blank=True)
    remarks = models.TextField(blank=True)
    gst_no = models.CharField(max_length=30, blank=True)
    phone_no = models.CharField(max_length=20, blank=True)
    email_id = models.EmailField(blank=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name    
    
class Broker(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    place = models.CharField(max_length=100, blank=True)
    phone_no = models.CharField(max_length=20, blank=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Confirmation(models.Model):
    confirmation_number = models.CharField(max_length=50, blank=True)
    confirmation_date = models.DateField()

    supplier = models.ForeignKey(Seller, on_delete=models.PROTECT)
    buyer = models.ForeignKey(Buyer, on_delete=models.PROTECT)

    supplier_place = models.CharField(max_length=100, blank=True)
    buyer_place = models.CharField(max_length=100, blank=True)

    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    quality = models.CharField(max_length=100, blank=True)
    count = models.CharField(max_length=50, blank=True)
    moisture = models.CharField(max_length=50, blank=True)
    gunny = models.CharField(max_length=100, blank=True)

    rate = models.DecimalField(max_digits=10, decimal_places=2)
    packing = models.CharField(max_length=100, blank=True)

    delivery_at = models.CharField(max_length=100, blank=True)
    date_of_delivery = models.DateField(blank=True, null=True)
    supplier_commission_rate = models.DecimalField(max_digits=10, decimal_places=2, default=20)
    buyer_commission_rate = models.DecimalField(max_digits=10, decimal_places=2, default=20)

    supplier_broker = models.ForeignKey(
        Broker,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="supplier_confirmations"
    )
    buyer_broker = models.ForeignKey(
        Broker,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="buyer_confirmations"
    )

    remarks = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.confirmation_number:
            year = self.confirmation_date.year

            if self.confirmation_date.month >= 4:
                fy_start = f"{year}-04-01"
                fy_end = f"{year + 1}-03-31"
            else:
                fy_start = f"{year - 1}-04-01"
                fy_end = f"{year}-03-31"

            confirmations = Confirmation.objects.filter(
                confirmation_date__range=[fy_start, fy_end]
            )

            max_number = 0

            for c in confirmations:
                try:
                    num = int(c.confirmation_number)
                    if num > max_number:
                        max_number = num
                except:
                    pass

            self.confirmation_number = str(max_number + 1)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.confirmation_number} - {self.supplier} → {self.buyer}"

class Shipment(models.Model):
    COMMODITY_CHOICES = [
        ("GROUNDNUT", "Groundnut"),
        ("MAIZE", "Maize"),
    ]

    shipment_date = models.DateField()
    commodity_type = models.CharField(max_length=20, choices=COMMODITY_CHOICES)
    seller = models.ForeignKey(Seller, on_delete=models.PROTECT)
    buyer = models.ForeignKey(Buyer, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_bags = models.PositiveIntegerField()
    vehicle_number = models.CharField(max_length=30, blank=True)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.commodity_type} - {self.seller} to {self.buyer}"
    
class Bill(models.Model):
    confirmation = models.OneToOneField(Confirmation, on_delete=models.PROTECT)

    bill_number = models.CharField(max_length=50)
    bill_date = models.DateField()

    number_of_bags = models.IntegerField()
    quantity = models.DecimalField(max_digits=12, decimal_places=2)

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    gst = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    lorry_advance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    lorry_number = models.CharField(max_length=50, blank=True)

    bill_amount = models.DecimalField(max_digits=12, decimal_places=2)
    packing_kg = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    amount_received = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    others = models.TextField(blank=True)

class Payment(models.Model):
    confirmation = models.ForeignKey(Confirmation, on_delete=models.PROTECT)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Payment - {self.confirmation.confirmation_number}"


class PaymentLine(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="lines")
    serial_no = models.IntegerField()
    date = models.DateField()
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.serial_no} - {self.description}"

    def __str__(self):
        return self.bill_number
