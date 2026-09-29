from django.urls import path

from django.urls import path
from .views import *

urlpatterns = [
    path('production-schedule/', ProductionScheduleAPIView.as_view(),name='Production-schedule'),
    path('production-schedule/<int:pk>/', ProductionScheduleAPIView.as_view() , name='Production-schedule-delete'),
    path("schedule-month-filter/", ScheduleMonthFilterAPIView.as_view(), name='Schedule-month-wise-data'),
    path('month-wise-invoice-report/',  MonthWiseInvoiceReportAPIView.as_view(), name='month-wise-invoice-report'),

    path('update-item-wise-min-max/', UpdateItemWiseMinMaxAPIView.as_view(),name='update-item-wise-min-max'),
    path('update-item-wise-min-max/<int:pk>/', UpdateItemWiseMinMaxAPIView.as_view(),name='update-item-wise-min-max-update-delete'),

    path('dispatch-plan/',DispatchPlanAPIView.as_view(),name='dispatch-plan'),
    path('dispatch-plan/<int:pk>/',DispatchPlanAPIView.as_view(),name='dispatch-plan-update-delete'),
    path('customer/list/',CustomerItemListView.as_view(),name='Customer-list'),
    path('salesorder-po-search/', SalesOrderSearchAPIView.as_view(), name='salesorder-Po-get'),
    path('dispatch-stock-wip/',LastOperationProdQtyAPI.as_view(),name='dispatch-stock-from-wip-lastoperation'),
]