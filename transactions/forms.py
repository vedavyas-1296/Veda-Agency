from django import forms
from .models import Seller, Buyer, Broker, Shipment, Confirmation, Bill, Payment, PaymentLine


class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "place": forms.TextInput(attrs={"class": "form-control"}),
            "zipcode": forms.TextInput(attrs={"class": "form-control"}),
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "gst_no": forms.TextInput(attrs={"class": "form-control"}),
            "phone_no": forms.TextInput(attrs={"class": "form-control"}),
            "email_id": forms.EmailInput(attrs={"class": "form-control"}),
        }


class BuyerForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "place": forms.TextInput(attrs={"class": "form-control"}),
            "zipcode": forms.TextInput(attrs={"class": "form-control"}),
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "gst_no": forms.TextInput(attrs={"class": "form-control"}),
            "phone_no": forms.TextInput(attrs={"class": "form-control"}),
            "email_id": forms.EmailInput(attrs={"class": "form-control"}),
        }

class BrokerForm(forms.ModelForm):
    class Meta:
        model = Broker
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "place": forms.TextInput(attrs={"class": "form-control"}),
            "zipcode": forms.TextInput(attrs={"class": "form-control"}),
            "phone_no": forms.TextInput(attrs={"class": "form-control"}),
        }
class ConfirmationForm(forms.ModelForm):
    class Meta:
        model = Confirmation
        exclude = ["confirmation_number"]
        widgets = {
            "confirmation_number": forms.TextInput(attrs={"class": "form-control"}),
            "confirmation_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),

            "supplier": forms.Select(attrs={"class": "form-control"}),
            "buyer": forms.Select(attrs={"class": "form-control"}),

            "supplier_place": forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
            "buyer_place": forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),

            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "quality": forms.TextInput(attrs={"class": "form-control"}),
            "count": forms.TextInput(attrs={"class": "form-control"}),
            "moisture": forms.TextInput(attrs={"class": "form-control"}),
            "gunny": forms.TextInput(attrs={"class": "form-control"}),

            "rate": forms.NumberInput(attrs={"class": "form-control"}),
            "packing": forms.TextInput(attrs={"class": "form-control"}),

            "delivery_at": forms.TextInput(attrs={"class": "form-control"}),
            "date_of_delivery": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "supplier_commission_rate": forms.NumberInput(attrs={"class": "form-control"}),
            "buyer_commission_rate": forms.NumberInput(attrs={"class": "form-control"}),

            "supplier_broker": forms.Select(attrs={"class": "form-control"}),
            "buyer_broker": forms.Select(attrs={"class": "form-control"}),

            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = "__all__"
        widgets = {
            "shipment_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "commodity_type": forms.Select(attrs={"class": "form-control"}),
            "seller": forms.Select(attrs={"class": "form-control"}),
            "buyer": forms.Select(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "rate": forms.NumberInput(attrs={"class": "form-control"}),
            "number_of_bags": forms.NumberInput(attrs={"class": "form-control"}),
            "vehicle_number": forms.TextInput(attrs={"class": "form-control"}),
            "commission": forms.NumberInput(attrs={"class": "form-control"}),
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = "__all__"
        widgets = {
            "confirmation": forms.Select(attrs={"class": "form-control"}),
            "bill_number": forms.TextInput(attrs={"class": "form-control"}),
            "bill_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),

            "number_of_bags": forms.NumberInput(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "readonly": "readonly"}),

            "amount": forms.NumberInput(attrs={"class": "form-control", "readonly": "readonly"}),
            "gst": forms.NumberInput(attrs={"class": "form-control"}),

            "lorry_advance": forms.NumberInput(attrs={"class": "form-control"}),
            "lorry_number": forms.TextInput(attrs={"class": "form-control"}),
            "packing_kg": forms.NumberInput(attrs={"class": "form-control"}),
            "bill_amount": forms.NumberInput(attrs={"class": "form-control"}),
            "amount_received": forms.NumberInput(attrs={"class": "form-control"}),

            "others": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
    def clean(self):
        cleaned_data = super().clean()

        bags = cleaned_data.get("number_of_bags") or 0
        packing = cleaned_data.get("packing_kg") or 0
        bill_amount = cleaned_data.get("bill_amount")

        if bags <= 0:
            self.add_error("number_of_bags", "No of bags must be greater than 0.")

        if packing <= 0:
            self.add_error("packing_kg", "Packing must be greater than 0.")

        if not bill_amount:
            self.add_error("bill_amount", "Bill amount is required.")

        return cleaned_data


    def clean_confirmation(self):
        confirmation = self.cleaned_data.get("confirmation")

        if self.instance.pk:
            exists = Bill.objects.filter(confirmation=confirmation).exclude(pk=self.instance.pk).exists()
        else:
            exists = Bill.objects.filter(confirmation=confirmation).exists()

        if exists:
            raise forms.ValidationError("Bill already exists for this confirmation.")

        return confirmation
    
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["confirmation"]
        widgets = {
            "confirmation": forms.Select(attrs={"class": "form-control"}),
        }


class PaymentLineForm(forms.ModelForm):
    class Meta:
        model = PaymentLine
        fields = ["serial_no", "date", "description", "amount"]
        widgets = {
            "serial_no": forms.NumberInput(attrs={"class": "form-control"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
        }