from django.shortcuts import render, redirect
from .models import Shipment
from .forms import ShipmentForm
from django.db.models import Sum
from .models import Shipment, Seller, Buyer, Broker, Confirmation, Bill, Payment, PaymentLine
from .forms import ShipmentForm, SellerForm, BuyerForm, BrokerForm, ConfirmationForm, BillForm, PaymentForm
from django.http import HttpResponse
import openpyxl
from .forms import ShipmentForm, SellerForm, BuyerForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import ProtectedError
from django.http import JsonResponse
from django.db.models import Sum
from django.db.models.functions import Cast
from django.db.models import IntegerField
from django.db.models import Q
from django.db.models import Sum
from django.http import JsonResponse
from django.db.models import Sum
from decimal import Decimal
from decimal import Decimal
from django.db.models import Sum

def shipment_list(request):
    shipments = Shipment.objects.all().order_by("-shipment_date")

    sellers = Seller.objects.all()
    buyers = Buyer.objects.all()

    seller = request.GET.get("seller")
    buyer = request.GET.get("buyer")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if seller:
        shipments = shipments.filter(seller_id=seller)

    if buyer:
        shipments = shipments.filter(buyer_id=buyer)

    if start_date:
        shipments = shipments.filter(shipment_date__gte=start_date)

    if end_date:
        shipments = shipments.filter(shipment_date__lte=end_date)

    from django.db.models import Sum

    totals = shipments.aggregate(
        total_quantity=Sum("quantity"),
        total_bags=Sum("number_of_bags"),
        total_commission=Sum("commission"),
    )

    return render(request, "transactions/shipment_list.html", {
        "shipments": shipments,
        "totals": totals,
        "shipment_count": shipments.count(),
        "sellers": sellers,
        "buyers": buyers,
    })


def add_shipment(request):
    if request.method == "POST":
        form = ShipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("shipment_list")
    else:
        form = ShipmentForm()

    return render(request, "transactions/add_shipment.html", {
        "form": form
    })

def export_excel(request):
    shipments = Shipment.objects.all()

    seller = request.GET.get("seller")
    buyer = request.GET.get("buyer")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if seller:
        shipments = shipments.filter(seller_id=seller)

    if buyer:
        shipments = shipments.filter(buyer_id=buyer)

    if start_date:
        shipments = shipments.filter(shipment_date__gte=start_date)

    if end_date:
        shipments = shipments.filter(shipment_date__lte=end_date)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Shipments"

    # Header row
    ws.append([
        "Date", "Commodity", "Seller", "Buyer",
        "Quantity", "Rate", "Bags", "Commission"
    ])

    # Data rows
    for s in shipments:
        ws.append([
            str(s.shipment_date),
            s.commodity_type,
            s.seller.name,
            s.buyer.name,
            float(s.quantity),
            float(s.rate),
            s.number_of_bags,
            float(s.commission),
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = "attachment; filename=shipments.xlsx"

    wb.save(response)
    return response

def add_supplier(request):
    if request.method == "POST":
        form = SellerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("supplier_list")
    else:
        form = SellerForm()

    return render(request, "transactions/add_supplier.html", {
        "form": form
    })


def add_buyer(request):
    if request.method == "POST":
        form = BuyerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("buyer_list")
    else:
        form = BuyerForm()

    return render(request, "transactions/add_buyer.html", {
        "form": form
    })

from .models import Seller, Buyer


def supplier_list(request):
    suppliers = Seller.objects.all().order_by("name")

    search = request.GET.get("search")

    if search:
        suppliers = suppliers.filter(name__icontains=search)

    return render(request, "transactions/supplier_list.html", {
        "suppliers": suppliers
    })


def buyer_list(request):
    buyers = Buyer.objects.all().order_by("name")

    search = request.GET.get("search")

    if search:
        buyers = buyers.filter(name__icontains=search)

    return render(request, "transactions/buyer_list.html", {
        "buyers": buyers
    })

def edit_supplier(request, supplier_id):
    supplier = get_object_or_404(Seller, id=supplier_id)

    if request.method == "POST":
        form = SellerForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect("supplier_list")
    else:
        form = SellerForm(instance=supplier)

    return render(request, "transactions/edit_supplier.html", {
        "form": form,
        "supplier": supplier
    })


def edit_buyer(request, buyer_id):
    buyer = get_object_or_404(Buyer, id=buyer_id)

    if request.method == "POST":
        form = BuyerForm(request.POST, instance=buyer)
        if form.is_valid():
            form.save()
            return redirect("buyer_list")
    else:
        form = BuyerForm(instance=buyer)

    return render(request, "transactions/edit_buyer.html", {
        "form": form,
        "buyer": buyer
    })


def edit_shipment(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)

    if request.method == "POST":
        form = ShipmentForm(request.POST, instance=shipment)
        if form.is_valid():
            form.save()
            return redirect("shipment_list")
    else:
        form = ShipmentForm(instance=shipment)

    return render(request, "transactions/edit_shipment.html", {
        "form": form,
        "shipment": shipment
    })

def delete_shipment(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)

    if request.method == "POST":
        shipment.delete()
        return redirect("shipment_list")

    return render(request, "transactions/delete_shipment.html", {
        "shipment": shipment
    })

def delete_supplier(request, supplier_id):
    supplier = get_object_or_404(Seller, id=supplier_id)

    if request.method == "POST":
        try:
            supplier.delete()
            messages.success(request, "Supplier deleted successfully.")
        except ProtectedError:
            messages.error(request, "Cannot delete supplier. It is used in shipments.")

        return redirect("supplier_list")

    return render(request, "transactions/delete_supplier.html", {
        "supplier": supplier
    })

def delete_buyer(request, buyer_id):
    buyer = get_object_or_404(Buyer, id=buyer_id)

    if request.method == "POST":
        try:
            buyer.delete()
            messages.success(request, "Buyer deleted successfully.")
        except ProtectedError:
            messages.error(request, "Cannot delete buyer. It is used in shipments.")

        return redirect("buyer_list")

    return render(request, "transactions/delete_buyer.html", {
        "buyer": buyer
    })

def broker_list(request):
    brokers = Broker.objects.all().order_by("name")

    search = request.GET.get("search")

    if search:
        brokers = brokers.filter(name__icontains=search)

    return render(request, "transactions/broker_list.html", {
        "brokers": brokers
    })


def add_broker(request):
    if request.method == "POST":
        form = BrokerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("broker_list")
    else:
        form = BrokerForm()

    return render(request, "transactions/add_broker.html", {
        "form": form
    })


def edit_broker(request, broker_id):
    broker = get_object_or_404(Broker, id=broker_id)

    if request.method == "POST":
        form = BrokerForm(request.POST, instance=broker)
        if form.is_valid():
            form.save()
            return redirect("broker_list")
    else:
        form = BrokerForm(instance=broker)

    return render(request, "transactions/edit_broker.html", {
        "form": form,
        "broker": broker
    })


def delete_broker(request, broker_id):
    broker = get_object_or_404(Broker, id=broker_id)

    if request.method == "POST":
        broker.delete()
        return redirect("broker_list")

    return render(request, "transactions/delete_broker.html", {
        "broker": broker
    })

confirmations = Confirmation.objects.annotate(
    num=Cast('confirmation_number', IntegerField())
).order_by('num')

from django.db.models.functions import Cast
from django.db.models import IntegerField

def confirmation_list(request):
    confirmations = Confirmation.objects.annotate(
        num=Cast("confirmation_number", IntegerField())
    ).order_by("num")
    search = request.GET.get("search")
    type_filter = request.GET.get("type")

    if search:
        if type_filter == "conf":
            confirmations = confirmations.filter(confirmation_number__icontains=search)

        elif type_filter == "supplier":
            confirmations = confirmations.filter(supplier__name__icontains=search)

        elif type_filter == "buyer":
            confirmations = confirmations.filter(buyer__name__icontains=search)

        else:
            confirmations = confirmations.filter(
            Q(confirmation_number__icontains=search) |
            Q(supplier__name__icontains=search) |
            Q(buyer__name__icontains=search)
        )

    suppliers = Seller.objects.all().order_by("name")
    buyers = Buyer.objects.all().order_by("name")

    supplier = request.GET.get("supplier")
    buyer = request.GET.get("buyer")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if supplier:
        confirmations = confirmations.filter(supplier_id=supplier)

    if buyer:
        confirmations = confirmations.filter(buyer_id=buyer)

    if start_date:
        confirmations = confirmations.filter(confirmation_date__gte=start_date)

    if end_date:
        confirmations = confirmations.filter(confirmation_date__lte=end_date)

    return render(request, "transactions/confirmation_list.html", {
        "confirmations": confirmations,
        "suppliers": suppliers,
        "buyers": buyers,
    })

def add_confirmation(request):
    if request.method == "POST":
        form = ConfirmationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("confirmation_list")
    else:
        form = ConfirmationForm()

    return render(request, "transactions/add_confirmation.html", {
        "form": form
    })


def edit_confirmation(request, confirmation_id):
    confirmation = get_object_or_404(Confirmation, id=confirmation_id)

    if request.method == "POST":
        form = ConfirmationForm(request.POST, instance=confirmation)
        if form.is_valid():
            form.save()
            return redirect("confirmation_list")
    else:
        form = ConfirmationForm(instance=confirmation)

    return render(request, "transactions/edit_confirmation.html", {
        "form": form,
        "confirmation": confirmation
    })


def delete_confirmation(request, confirmation_id):
    confirmation = get_object_or_404(Confirmation, id=confirmation_id)

    if request.method == "POST":
        try:
            confirmation.delete()
            messages.success(request, "Confirmation deleted successfully.")
        except ProtectedError:
            messages.error(request, "Cannot delete confirmation. A bill already exists for this confirmation.")

        return redirect("confirmation_list")

    return render(request, "transactions/delete_confirmation.html", {
        "confirmation": confirmation
    })

def print_confirmation(request, confirmation_id):
    confirmation = get_object_or_404(Confirmation, id=confirmation_id)

    return render(request, "transactions/print_confirmation.html", {
        "confirmation": confirmation
    })

def bill_list(request):
    bills = Bill.objects.select_related("confirmation").annotate(
        num=Cast("confirmation__confirmation_number", IntegerField())
    ).order_by("num")

    suppliers = Seller.objects.all().order_by("name")
    buyers = Buyer.objects.all().order_by("name")

    supplier = request.GET.get("supplier")
    buyer = request.GET.get("buyer")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    search = request.GET.get("search")
    type_filter = request.GET.get("type")

    if search:
        if type_filter == "bill":
            bills = bills.filter(bill_number__icontains=search)
        elif type_filter == "conf":
            bills = bills.filter(confirmation__confirmation_number__icontains=search)
        elif type_filter == "supplier":
            bills = bills.filter(confirmation__supplier__name__icontains=search)
        elif type_filter == "buyer":
            bills = bills.filter(confirmation__buyer__name__icontains=search)
        else:
            bills = bills.filter(
                Q(bill_number__icontains=search) |
                Q(confirmation__confirmation_number__icontains=search) |
                Q(confirmation__supplier__name__icontains=search) |
                Q(confirmation__buyer__name__icontains=search)
        )

    if supplier:
        bills = bills.filter(confirmation__supplier_id=supplier)

    if buyer:
        bills = bills.filter(confirmation__buyer_id=buyer)

    if start_date:
        bills = bills.filter(bill_date__gte=start_date)

    if end_date:
        bills = bills.filter(bill_date__lte=end_date)

    return render(request, "transactions/bill_list.html", {
        "bills": bills,
        "suppliers": suppliers,
        "buyers": buyers,
    })

def add_bill(request):
    if request.method == "POST":
        form = BillForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("bill_list")
    else:
        form = BillForm()

    return render(request, "transactions/add_bill.html", {
        "form": form
    })


def edit_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)

    if request.method == "POST":
        form = BillForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            return redirect("bill_list")
    else:
        form = BillForm(instance=bill)

    return render(request, "transactions/edit_bill.html", {
        "form": form,
        "bill": bill
    })


def delete_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)

    if request.method == "POST":
        bill.delete()
        return redirect("bill_list")

    return render(request, "transactions/delete_bill.html", {
        "bill": bill
    })

from django.http import JsonResponse

def get_confirmation_data(request, confirmation_id):
    c = get_object_or_404(Confirmation, id=confirmation_id)

    data = {
        "supplier": str(c.supplier),
        "buyer": str(c.buyer),
        "supplier_place": c.supplier_place,
        "buyer_place": c.buyer_place,
        "quantity": float(c.quantity),
        "rate": float(c.rate),
        "bill_exists": hasattr(c, "bill"),
    }

    return JsonResponse(data)

def print_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)

    return render(request, "transactions/print_bill.html", {
        "bill": bill
    })
def dashboard(request):
    total_suppliers = Seller.objects.count()
    total_buyers = Buyer.objects.count()
    total_brokers = Broker.objects.count()
    total_confirmations = Confirmation.objects.count()
    total_bills = Bill.objects.count()

    total_bill_amount = Bill.objects.aggregate(Sum("bill_amount"))["bill_amount__sum"] or 0
    total_received = Bill.objects.aggregate(Sum("amount_received"))["amount_received__sum"] or 0
    pending_amount = total_bill_amount - total_received

    return render(request, "transactions/dashboard.html", {
        "total_suppliers": total_suppliers,
        "total_buyers": total_buyers,
        "total_brokers": total_brokers,
        "total_confirmations": total_confirmations,
        "total_bills": total_bills,
        "total_bill_amount": total_bill_amount,
        "total_received": total_received,
        "pending_amount": pending_amount,
    })
def get_party_details(request):
    supplier_id = request.GET.get("supplier_id")
    buyer_id = request.GET.get("buyer_id")

    data = {}

    if supplier_id:
        supplier = Seller.objects.get(id=supplier_id)
        data["supplier_place"] = supplier.place

    if buyer_id:
        buyer = Buyer.objects.get(id=buyer_id)
        data["buyer_place"] = buyer.place

    return JsonResponse(data)

def reports(request):
    total_amount = Bill.objects.aggregate(total=Sum("bill_amount"))["total"] or 0
    total_received = Bill.objects.aggregate(total=Sum("amount_received"))["total"] or 0

    pending = total_amount - total_received

    return render(request, "transactions/reports.html", {
        "total_amount": total_amount,
        "total_received": total_received,
        "pending": pending,
    })
def payment_list(request):
    payments = Payment.objects.select_related("confirmation").all().order_by("-created_date")

    search = request.GET.get("search")

    if search:
        payments = payments.filter(
            Q(confirmation__confirmation_number__icontains=search) |
            Q(confirmation__supplier__name__icontains=search) |
            Q(confirmation__buyer__name__icontains=search)
        )

    return render(request, "transactions/payment_list.html", {
        "payments": payments
    })

def add_payment(request):
    confirmations = Confirmation.objects.all().order_by("confirmation_number")

    if request.method == "POST":
        form = PaymentForm(request.POST)

        if form.is_valid():
            payment = form.save()

            serials = request.POST.getlist("serial_no")
            dates = request.POST.getlist("date")
            descriptions = request.POST.getlist("description")
            amounts = request.POST.getlist("amount")

            for i in range(len(serials)):
                if serials[i] and dates[i] and descriptions[i] and amounts[i]:
                    PaymentLine.objects.create(
                        payment=payment,
                        serial_no=serials[i],
                        date=dates[i],
                        description=descriptions[i],
                        amount=amounts[i],
                    )

            return redirect("payment_list")
    else:
        form = PaymentForm()

    return render(request, "transactions/add_payment.html", {
        "form": form,
        "confirmations": confirmations
    })


def delete_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)

    if request.method == "POST":
        payment.delete()
        return redirect("payment_list")

    return render(request, "transactions/delete_payment.html", {
        "payment": payment
    })

def edit_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)

    if request.method == "POST":
        form = PaymentForm(request.POST, instance=payment)

        if form.is_valid():
            payment = form.save()

            # Remove old lines and recreate from submitted table
            payment.lines.all().delete()

            serials = request.POST.getlist("serial_no")
            dates = request.POST.getlist("date")
            descriptions = request.POST.getlist("description")
            amounts = request.POST.getlist("amount")

            for i in range(len(serials)):
                if serials[i] and dates[i] and descriptions[i] and amounts[i]:
                    PaymentLine.objects.create(
                        payment=payment,
                        serial_no=serials[i],
                        date=dates[i],
                        description=descriptions[i],
                        amount=amounts[i],
                    )

            return redirect("payment_list")
    else:
        form = PaymentForm(instance=payment)

    return render(request, "transactions/edit_payment.html", {
        "form": form,
        "payment": payment,
    })

def view_confirmation(request, confirmation_id):
    confirmation = get_object_or_404(Confirmation, id=confirmation_id)

    return render(request, "transactions/view_confirmation.html", {
        "confirmation": confirmation
    })

def view_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)

    return render(request, "transactions/view_bill.html", {
        "bill": bill
    })
def view_supplier(request, supplier_id):
    supplier = get_object_or_404(Seller, id=supplier_id)

    return render(request, "transactions/view_supplier.html", {
        "supplier": supplier
    })


def view_buyer(request, buyer_id):
    buyer = get_object_or_404(Buyer, id=buyer_id)

    return render(request, "transactions/view_buyer.html", {
        "buyer": buyer
    })


def view_broker(request, broker_id):
    broker = get_object_or_404(Broker, id=broker_id)

    return render(request, "transactions/view_broker.html", {
        "broker": broker
    })

def get_payment_details(request, confirmation_id):
    confirmation = get_object_or_404(Confirmation, id=confirmation_id)

    try:
        bill = Bill.objects.get(confirmation=confirmation)
    except Bill.DoesNotExist:
        return JsonResponse({
            "error": "No bill found for this confirmation."
        }, status=404)

    paid_amount = PaymentLine.objects.filter(
        payment__confirmation=confirmation
    ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    bill_amount = bill.bill_amount or Decimal("0.00")
    balance_amount = bill_amount - paid_amount

    return JsonResponse({
        "confirmation_number": confirmation.confirmation_number,
        "supplier": str(confirmation.supplier),
        "buyer": str(confirmation.buyer),
        "supplier_place": confirmation.supplier_place,
        "buyer_place": confirmation.buyer_place,

        "bill_number": bill.bill_number,
        "bill_date": bill.bill_date.strftime("%Y-%m-%d") if bill.bill_date else "",
        "quantity": str(bill.quantity),
        "bill_amount": str(bill_amount),
        "paid_amount": str(paid_amount),
        "balance_amount": str(balance_amount),
        "lorry_number": bill.lorry_number,
    })

def commission_report(request):
    party_type = request.GET.get("party_type")
    party_id = request.GET.get("party")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    suppliers = Seller.objects.all().order_by("name")
    buyers = Buyer.objects.all().order_by("name")

    report_rows = []
    total_commission = Decimal("0.00")

    bills = Bill.objects.select_related(
        "confirmation",
        "confirmation__supplier",
        "confirmation__buyer"
    ).all().order_by("bill_date")

    if start_date:
        bills = bills.filter(bill_date__gte=start_date)

    if end_date:
        bills = bills.filter(bill_date__lte=end_date)

    selected_party_name = ""

    if party_type == "supplier" and party_id:
        bills = bills.filter(confirmation__supplier_id=party_id)
        selected_party = Seller.objects.filter(id=party_id).first()
        selected_party_name = selected_party.name if selected_party else ""

    elif party_type == "buyer" and party_id:
        bills = bills.filter(confirmation__buyer_id=party_id)
        selected_party = Buyer.objects.filter(id=party_id).first()
        selected_party_name = selected_party.name if selected_party else ""

    if party_type and party_id:
        for bill in bills:
            confirmation = bill.confirmation

            quantity_kg = bill.quantity or Decimal("0.00")
            quantity_quintal = quantity_kg / Decimal("100")

            if party_type == "supplier":
                commission_rate = confirmation.supplier_commission_rate or Decimal("0.00")
            else:
                commission_rate = confirmation.buyer_commission_rate or Decimal("0.00")

            commission_amount = quantity_quintal * commission_rate
            total_commission += commission_amount

            report_rows.append({
                "confirmation_no": confirmation.confirmation_number,
                "confirmation_date": confirmation.confirmation_date,
                "bill_no": bill.bill_number,
                "bill_date": bill.bill_date,
                "supplier": confirmation.supplier,
                "buyer": confirmation.buyer,
                "quantity_kg": quantity_kg,
                "quantity_quintal": quantity_quintal,
                "commission_rate": commission_rate,
                "commission_amount": commission_amount,
            })

    return render(request, "transactions/commission_report.html", {
        "suppliers": suppliers,
        "buyers": buyers,
        "party_type": party_type,
        "party_id": party_id,
        "start_date": start_date,
        "end_date": end_date,
        "selected_party_name": selected_party_name,
        "report_rows": report_rows,
        "total_commission": total_commission,
    })