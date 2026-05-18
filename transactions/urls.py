from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("shipments/", views.shipment_list, name="shipment_list"),
    path("add/", views.add_shipment, name="add_shipment"),
    path("add-supplier/", views.add_supplier, name="add_supplier"),
    path("add-buyer/", views.add_buyer, name="add_buyer"),
    path("export/", views.export_excel, name="export_excel"),
    path("suppliers/", views.supplier_list, name="supplier_list"),
    path("buyers/", views.buyer_list, name="buyer_list"),
    path("supplier/<int:supplier_id>/edit/", views.edit_supplier, name="edit_supplier"),
    path("buyer/<int:buyer_id>/edit/", views.edit_buyer, name="edit_buyer"),
    path("shipment/<int:shipment_id>/edit/", views.edit_shipment, name="edit_shipment"),
    path("shipment/<int:shipment_id>/delete/", views.delete_shipment, name="delete_shipment"),
    path("supplier/<int:supplier_id>/delete/", views.delete_supplier, name="delete_supplier"),
    path("buyer/<int:buyer_id>/delete/", views.delete_buyer, name="delete_buyer"),
    path("brokers/", views.broker_list, name="broker_list"),
    path("add-broker/", views.add_broker, name="add_broker"),
    path("broker/<int:broker_id>/edit/", views.edit_broker, name="edit_broker"),
    path("broker/<int:broker_id>/delete/", views.delete_broker, name="delete_broker"),
    path("confirmations/", views.confirmation_list, name="confirmation_list"),
    path("add-confirmation/", views.add_confirmation, name="add_confirmation"),
    path("confirmation/<int:confirmation_id>/edit/", views.edit_confirmation, name="edit_confirmation"),
    path("confirmation/<int:confirmation_id>/delete/", views.delete_confirmation, name="delete_confirmation"),
    path("confirmation/<int:confirmation_id>/print/", views.print_confirmation, name="print_confirmation"),
    path("bills/", views.bill_list, name="bill_list"),
    path("add-bill/", views.add_bill, name="add_bill"),
    path("bill/<int:bill_id>/edit/", views.edit_bill, name="edit_bill"),
    path("bill/<int:bill_id>/delete/", views.delete_bill, name="delete_bill"),
    path("get-confirmation/<int:confirmation_id>/", views.get_confirmation_data),
    path("bill/<int:bill_id>/print/", views.print_bill, name="print_bill"),
    path("get-party-details/", views.get_party_details),
    path("reports/", views.reports, name="reports"),
    path("payments/", views.payment_list, name="payment_list"),
    path("add-payment/", views.add_payment, name="add_payment"),
    path("payment/<int:payment_id>/delete/", views.delete_payment, name="delete_payment"),
    path("payment/<int:payment_id>/edit/", views.edit_payment, name="edit_payment"),
    path("confirmation/<int:confirmation_id>/view/", views.view_confirmation, name="view_confirmation"),
    path("bill/<int:bill_id>/view/", views.view_bill, name="view_bill"),
    path("supplier/<int:supplier_id>/view/", views.view_supplier, name="view_supplier"),
    path("buyer/<int:buyer_id>/view/", views.view_buyer, name="view_buyer"),
    path("broker/<int:broker_id>/view/", views.view_broker, name="view_broker"),
    path("get-payment-details/<int:confirmation_id>/", views.get_payment_details, name="get_payment_details"),
    path("commission-report/", views.commission_report, name="commission_report"),



    
    

    
    

    
    
    ]


