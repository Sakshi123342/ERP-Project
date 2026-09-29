from django.urls import path
from .views import *

urlpatterns = [
     path('assessable-report/', AssessableValueReport.as_view(), name='assessable-report'),
     path('monthly/daily/report/',AssessableMonthlyReport.as_view() , name='Tax-invocice-monthly-report'),
     path('Top/5/Customer/',TopCustomersReport.as_view(), name="Top-5-customer-Invoice" ),
     path('itemwise/data/', CustomerDescriptionSummary.as_view(), name='Item-wise-data'),
     path('bussiness-invoice-summary/',BussinessSummaryAPIView.as_view(),name='month-wise-invoice-summary'),
     path("top-5-region-sales/", Top5RegionSalesAPIView.as_view(),name="top-5-region-sales",),
     path("bussiness-invoice-value/",BusinessSummaryValueAPIView.as_view(),name='Monthly-bussiness-plan-value'),

     #Purchase Dashboard API
     path("purchase/purchase-po-summary/",PurchasePOSeriesSummaryAPIView.as_view(), name="purchase-po-series-summary"),
     path( "financial-grn-total/", FinancialYearGrnTotalAPIView.as_view(),  name="financial-grn-total-month-wise"),
     path("Purchase/grn-monthly-total/", MonthlyGrnTotalAPIView.as_view(), name="grn-monthly-total"),
     path("top-five-suppliers/", TopFiveSupplierAPIView.as_view(), name="top-five-suppliers"), 
     path("item-wise-grn-report/",ItemWiseGrnReportAPIView.as_view(),name="item-wise-grn-report"),
     path("main-group-wise-grn-report/",MainGroupWiseGrnReportAPIView.as_view(), name="main-group-wise-grn-report"),


     # PPC Dashboard API
     path("ppc/schqty/month/wise/",MonthWiseScheduleQtyAPIView.as_view(),name='SchQty-from-productionshedule'),

     # Store
     path("store/inward/",InwardMonthlyEntryAPIView.as_view(),name="Inward-monthly"),
     path("store/outward/",OutwardMonthlyEntryAPIView.as_view(),name="Outward-monthly"),

     path(
        "min-max/",
        UpdateItemWiseMinMaxAPIView.as_view(),
        name="update-item-wise-min-max",
    ),
    path("fgitem",FGItemListAPIView.as_view(),),
    path("store/min-max/level",ItemMasterAPIView.as_view(),name='minmax-level'),


    # Quality
    path("Quality/rework_qty/",ProductionReworkReportAPIView.as_view(),name="Production-rework-qty-datewise"),
    path("Quality/reject_qty/",ProductionRejectReportAPIView.as_view(),name='Production-Reject_qty-datewise'),
    path("Quality/trend_rejection/",ProductionRejectMonthWiseAPIView.as_view(),name="Trend_of_rejec_qty_alldays-of-month"),
    path("Quality/scrap/qty/",ScrapRejectMonthTotalAPIView.as_view(),name="Scrape-Qty-from-production"),
    path("Quality/sales-return/",SalesReturnFinancialYearAPIView.as_view(),name="gst-sales-return"),

]
    