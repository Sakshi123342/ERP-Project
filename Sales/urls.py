from rest_framework.routers import DefaultRouter
from .views import OnwardChallanViewSet
from django.urls import path
from .views import generate_unique_challan_number,generate_unique_rework_number
from .views import deletechallan 
from .views import transportdetailsview
from .views import deletetransportdetails
from .views import edittransportdetails
from .views import vehicaldetailsview 
from .views import deletevehicaldetails 
from .views import editvehicaldetails
from .views import purchaseview
from .views import inwardchallanview,InwardChallanRMView
from .views import outwardchallanview
from .views import supplierview 
from .views import ItemFullReport
from .import views 
from .views import *


router = DefaultRouter()
router.register(r'onwardchallan', OnwardChallanViewSet)
router.register(r'transportdetails', transportdetailsview)
router.register(r'vehicaldetails', vehicaldetailsview)
router.register(r'outwardchallan',outwardchallanview)
router.register(r'onward-challans', OnwardChallanViewSet, basename='onward-challan')
router.register(r'invoice', InvoiceViewSet, basename='invoice')
router.register(r'newsalesorder' ,NewsalesOrederViewSet, basename='NewSalesOreder')
router.register(r'debitnote',DebitNoteViewSet,basename='Debit-note')
router.register(r'Gstsalesretun', NewgstsalesreturnViewSet, basename='New-Gst-Sales-Return')
router.register(r'gst-jobwork-invoice',GSTJobworkInvoiceViewSet , basename='GST-Jobwork-Invoice')


urlpatterns=router.urls+[
   path("generate-challan-no/", generate_unique_challan_number.as_view(), name='generate-challan-no'),
   path("deletechallan/<int:id>/",deletechallan.as_view(), name="deletechallan"),
   path("deletetransportdetails/<str:name>/",deletetransportdetails.as_view() , name="deletetransportdetails"),
   path("edittransportdetails/<str:name>/",edittransportdetails.as_view(), name='edittransportdetails'),
   path('deletevehicaldetails/<str:name>',deletevehicaldetails.as_view(),name='deletevehicaldetails'),
   path('editvehicaldetails/<str:vehical_no>', editvehicaldetails.as_view(), name='editvehicaldetails'),
   path('purchaseview/',purchaseview.as_view(),name='purchaseview'),
   path('inwardchallanview/',inwardchallanview.as_view(),name='inwardchallanview'),
#    /sales/inwardchallanview/?supplier=SUPPLIER_NAME
#    path('inward/', views.inward, name='inward'),
    path('supplierview/',supplierview.as_view(),name='onwardchallandetails-by-supplier'),
    path('onwardchallan/pdf/<int:pk>/', views.generate_onwardchallan_pdf,name='pdf'),

    path('inwardchallanrmview/',InwardChallanRMView.as_view(), name="inwardcahllan-rm-views"),
    path("genrate-rework-no",generate_unique_rework_number.as_view(),name='Genrate-Rework-number'),

    path('heatno/fg/',ItemFullReport.as_view() ,name="sales-fg-heat-no-stockwise" ),
    path('items/customers-list/', CustomerItemListView.as_view(),name="Custerm-view-for-newsales-order"),

    path('items-list/', ItemTableListView.as_view(), name='item-table-list'),

    path('create/invoice_no',generate_invoice_number.as_view(), name='create-invoice-no-for-gst-invoice'),
    
    path('wip/stock/get/',LastOperationProdQtyAPI.as_view(),name='wip-stcok-last-opno-stcok-get'),
    path('debit/no', GenerateDebitNoteNumber.as_view(), name='genrate-debit-note-no'),
    path("purchase-po/by-supplier/", PurchasePOBySupplierAPIView.as_view(), name='debit-note-purchase-grn-data'),

    path('sales/return-no/', GenerateSalesReturnNumber.as_view(), name='Gst-sales-return-no-genrate'),

    path('debit-note/<int:pk>/', DebitNotePDFAPIView.as_view(), name='purchase-debit-note-pdf-genrater'),

    path("customer/po/", NewSalesOrderListAPIView.as_view(), name="customer-po-for-gstinvoice"),

    path("salesreturn/gate-entry", SalesReturnListAPIView.as_view(), name="sales-return-list"),

    path("generate-so-no/", GenerateSalesOrderNumber.as_view(), name="generate-so-no-for-newsalesoreder"),

    path("finish-op-heat-wise/",FinishOpHeatWiseProd.as_view(),name="finish-op-heat-wise"),

    path("sales-return-pdf/<int:pk>/", generate_salesreturn_pdf, name="generate_salesreturn_pdf"),
    path("get/sales-return/" ,GetNewgstsalesreturn.as_view(), name='Get-Sales-retun-data-with-datewise'),
    path('invoice-pdf/<int:pk>/', generate_invoice_pdf, name='invoice-pdf'),

    path('sales-rate-diff/', SalesRateDiffAPI.as_view(), name='Sales-rate-diff'),
    path('sales-rate-diff/<int:pk>/', SalesRateDiffAPI.as_view() , name='sales-diff-Update-Delete'),
    path("sales-diff/no/",GenrateDebitNoteNoforsalesDiff.as_view(), name ='sales-diff-debit-No'),

    path("sales-diff/invoice/", InvoiceFilterAPI.as_view(), name='sales-diff-Invoice-data'),

    path('gstjobwork/invoice/no/',GenerateGSTJobworkInvoiceNo.as_view(),name='Gst-Jobwork-Invoice-no-genrate'),
    path('gst-jobwork-rate-diff/', GSTJobworkRateDiffAPIView.as_view(),name='gst-jobwork-rate-diff-create'),
    path('gst-jobwork-rate-diff/<int:pk>/', GSTJobworkRateDiffDetailAPIView.as_view(),name='Gst-jobwork-rate-diff-updated-delete'),
    path('Gst-jobwork-diff/no/',GenerateGSTJobworkRateDiffDebitNoteNo.as_view(),name='Gst-jobwork-ratediff-no-genrate'),
    path('gst/jobwork/invoice/filter/', GSTJobworkInvoiceFilterAPIView.as_view(), name='gst-jobwork-invoice-filter'  ),
    path('gst-jobwork-invoice-pdf/<int:pk>/', generate_gstjobwork_invoice_pdf, name='gst-jobwork-invoice-pdf'),

    path('customer-po-amendment/', CustomerPoAmendmentAPIView.as_view(),name='customer-po-amendment-post-get'),
    path('customer-po-amd-no/', GenerateCustomerPoAmdNo.as_view(), name='generate-customre-po-amd-no'),

    path('outwardchallan/fg/stock/',ProductionByOutAndInPart.as_view(),name='outchallan-fg-stockfrom-wip-okqty'),

    path('credit-note/', CreditNoteAPIView.as_view(),name='Credit-Note-Create'),
    path('generate-credit-note-no/', GenerateCreditNoteNo.as_view(), name='generate-credit-note-no'),
    path('credit-note-pdf/<int:pk>/', generate_credit_note_pdf, name='credit_note_pdf'),
    path('profoma-invoice/', NewProfomaInvoiceAPIView.as_view(), name='profoma-invoice'),
    path('profoma-invoice/<int:pk>/',NewProfomaInvoiceAPIView.as_view(),name='profoma-invoice-detail'),
    path("generate-invoice-no/",  GenerateInvoiceNo.as_view(), name="generate-invoice-no"),

    path('heat/',HeatAPIView.as_view()),
]
