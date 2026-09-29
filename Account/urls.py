from django.urls import path

from django.urls import path
from .views import *

urlpatterns = [
    path('invoice/date-filter/',InvoiceDateFilterAPIView.as_view(),name='Sales-GSTinvoice-date-filter'),
    path('pending-bill-grn/', PendingBillGrnlistAPIView.as_view(),name='pending-bill-grn'),
    path('purchase-po-date-filter/', GrnDateFilterAPIView.as_view(), name='purchase-po-for-pendingbillgrn'),
    path('bill-register/', BillRegisterAPIView.as_view(), name='bill-register'),   
    path('bill-register/<int:pk>/', BillRegisterAPIView.as_view(), name='bill-register-detail'),
    path('generate-bill-no/', GenerateBillNumberAPIView.as_view(), name='generate-bill-no'),
    path('inwardchllan-date-fillter/',InwardChallanDateFilterAPIView.as_view(),name='Inward-challan-date-supplier-filter'),

    path('jobwork-bill-register/',JobworkBillRegisterAPIView.as_view(),name='jobwork-bill-register'),
    path('jobwork-bill-register/<int:pk>/', JobworkBillRegisterAPIView.as_view(),name='jobwork-bill-register-delete-update' ),
    path('genrate-jobwork-bill-no/',GeneratejobworkBillNumberAPIView.as_view(),name='genrate-jobwork-billno'),
    path("bill-register-pdf/<int:pk>/",  generate_billregister_pdf,  name="Purchase-bill-register-pdf"),
    path('generate-jobworkbill-pdf/<int:id>/',generate_jobwork_pdf, name='generate-Inwardchallan-pdf'),
   path("jobwork-bill-pdf/<int:pk>/", generate_jobwork_bill_pdf, name="generate_jobwork_bill_pdf"),
   path('purchasebillpdf/<int:id>/', generate_purchase_grn_pdf, name='purchase-grn-pdf'  ),
   path('general-ledger/', GeneralLedgerMasterAPIView.as_view(), name='general-ledger-list-create'),
   path('general-ledger/<int:pk>/', GeneralLedgerMasterAPIView.as_view(), name='general-ledger-detail-updated-delete'),
   path("hsn-summary/", HSNSummaryAPIView.as_view(), name="hsn-summary"),
]