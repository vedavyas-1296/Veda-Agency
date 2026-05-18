from django.contrib import admin
from .models import Seller, Buyer, Broker, Shipment, Confirmation, Bill, Payment, PaymentLine



@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ("name", "place", "phone_no", "gst_no", "email_id")
    search_fields = ("name", "place", "phone_no", "gst_no", "email_id")


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ("name", "place", "phone_no", "gst_no", "email_id")
    search_fields = ("name", "place", "phone_no", "gst_no", "email_id")

@admin.register(Broker)
class BrokerAdmin(admin.ModelAdmin):
    list_display = ("name", "place", "phone_no")
    search_fields = ("name", "place", "phone_no")
@admin.register(Confirmation)
class ConfirmationAdmin(admin.ModelAdmin):
    list_display = (
        "confirmation_number",
        "confirmation_date",
        "supplier",
        "buyer",
        "quantity",
        "rate",
        "date_of_delivery",
    )
    search_fields = (
        "confirmation_number",
        "supplier__name",
        "buyer__name",
        "supplier_broker__name",
        "buyer_broker__name",
    )
    list_filter = ("confirmation_date", "date_of_delivery", "supplier", "buyer")
@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = (
        "shipment_date",
        "commodity_type",
        "seller",
        "buyer",
        "quantity",
        "rate",
        "number_of_bags",
        "commission",
    )
    list_filter = ("commodity_type", "shipment_date", "seller", "buyer")
    search_fields = (
        "seller__name",
        "buyer__name",
        "vehicle_number",
        "remarks",
    )
    date_hierarchy = "shipment_date"

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ("bill_number", "bill_date", "confirmation", "quantity", "bill_amount")
    search_fields = ("bill_number", "confirmation__confirmation_number")

class PaymentLineInline(admin.TabularInline):
    model = PaymentLine
    extra = 1


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("confirmation", "created_date")
    inlines = [PaymentLineInline]