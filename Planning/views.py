from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *


class ProductionScheduleAPIView(APIView):

    # ✅ GET (All Data)
    def get(self, request):
        queryset = ProductionSchedule.objects.all().order_by('-id')
        serializer = ProductionScheduleSerializer(queryset, many=True)

        return Response({
            "message": "Data fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    

    def post(self, request):
        print("DATA AA RHA HAI:", request.data)   # 👈 check input

        serializer = ProductionScheduleSerializer(data=request.data)

        if serializer.is_valid():
            obj = serializer.save()

            print("SAVE HO GYA:", obj.id)   # 👈 check saved id

            return Response({
                "message": "Created successfully",
                "data": serializer.data
            }, status=201)

        print("ERROR AA RHA HAI:", serializer.errors)  # 👈 main debug
        return Response(serializer.errors, status=400)
    # ✅ POST (Create)
    # def post(self, request):
    #     serializer = ProductionScheduleSerializer(data=request.data)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({
    #             "message": "Created successfully",
    #             "data": serializer.data
    #         }, status=status.HTTP_201_CREATED)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # ✅ PUT (Update by ID)
    def put(self, request, pk):
        obj = get_object_or_404(ProductionSchedule, pk=pk)

        serializer = ProductionScheduleSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # ✅ DELETE (Delete by ID)
    def delete(self, request, pk):
        obj = get_object_or_404(ProductionSchedule, pk=pk)
        obj.delete()

        return Response({
            "message": "Deleted successfully"
        }, status=status.HTTP_200_OK)
    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Settings.models import ScheduleMonthMaster
from Settings.serializers import ScheduleMonthSerializer

class ScheduleMonthFilterAPIView(APIView):

    def get(self, request):
        month_name = request.query_params.get("month_name")   # e.g. MARCH 2026

        queryset = ScheduleMonthMaster.objects.all()

        if month_name:
            queryset = queryset.filter(month_name__iexact=month_name)

        serializer = ScheduleMonthSerializer(queryset, many=True)

        return Response({
            "message": "Filtered data fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.db.models.functions import Coalesce
from Sales.models import InvoiceItemdetails


# class MonthWiseInvoiceReportAPIView(APIView):

#     def get(self, request):
#         month = request.query_params.get("month")  # example: 4
#         year = request.query_params.get("year")    # example: 2026

#         # Validation
#         if not month or not year:
#             return Response(
#                 {
#                     "error": "month and year are required"
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         try:
#             month = int(month)
#             year = int(year)
#         except ValueError:
#             return Response(
#                 {
#                     "error": "month and year must be integer"
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Main Query
#         data = (
#             InvoiceItemdetails.objects
#             .filter(
#                 invoice__invoice_Date__month=month,
#                 invoice__invoice_Date__year=year
#             )
#             .values(
#                 'part_no',
#                 'part_code',
#                 'description'
#             )
#             .annotate(
#                 total_inv_qty=Sum('inv_qty')
#             )
#             .order_by('part_no')
#         )

#         return Response(
#             {
#                 "message": "Month wise invoice data fetched successfully",
#                 "month": month,
#                 "year": year,
#                 "data": data
#             },
#             status=status.HTTP_200_OK
#         )



# from django.db.models import Sum, IntegerField, Value
# class MonthWiseInvoiceReportAPIView(APIView):
#     def get(self, request):
#         month = request.query_params.get("month")
#         year = request.query_params.get("year")

#         if not month or not year:
#             return Response(
#                 {
#                     "error": "month and year are required"
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

    
#         schedule_data = (
#             ProductionSchedule.objects
#             .filter(
#                 schedule_month__month_no=month,
#                 schedule_month__year_no=year
#             )
#             .values(
#                 'item_no',
#                 'item_code',
#                 'item_description'
#             )
#             .annotate(
#                 total_sch_qty=Coalesce(
#                     Sum('sch_qty', output_field=IntegerField()),
#                     Value(0)
#                 )
#             )
#         )

#         final_data = []

#         for schedule in schedule_data:

#             item_no = schedule['item_no']
#             item_code = schedule['item_code']
#             item_description = schedule['item_description']
#             total_sch_qty = schedule['total_sch_qty'] or 0

#             # ============================
#             # Invoice Qty Total
#             # ============================
#             invoice_qty = (
#                 InvoiceItemdetails.objects
#                 .filter(
#                     invoice__invoice_Date__month=month,
#                     invoice__invoice_Date__year=year,
#                     part_no=item_no,
#                     part_code=item_code,
#                     description=item_description
#                 )
#                 .aggregate(
#                     total_inv_qty=Coalesce(
#                         Sum('inv_qty'),
#                         Value(0)
#                     )
#                 )
#             )

#             total_inv_qty = invoice_qty['total_inv_qty'] or 0

#             # ============================
#             # Balance Qty
#             # ============================
#             bal_qty = int(total_sch_qty) - int(total_inv_qty)

#             final_data.append({
#                 "item_no": item_no,
#                 "item_code": item_code,
#                 "item_description": item_description,
#                 "sch_qty": total_sch_qty,
#                 "total_inv_qty": total_inv_qty,
#                 "bal_qty": bal_qty
#             })

#         return Response(
#             {
#                 "message": "Month wise balance report fetched successfully",
#                 "month": month,
#                 "year": year,
#                 "data": final_data
#             },
#             status=status.HTTP_200_OK
#         )
from django.db.models import Sum, IntegerField, Value
from django.db.models.functions import Coalesce
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import date, timedelta
import calendar


class MonthWiseInvoiceReportAPIView(APIView):

    def get(self, request):

        month = request.query_params.get("month")
        year = request.query_params.get("year")

        # =========================================
        # Validation
        # =========================================

        if not month or not year:
            return Response(
                {
                    "error": "month and year are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            month = int(month)
            year = int(year)

        except ValueError:
            return Response(
                {
                    "error": "month and year must be integer"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # =========================================
        # Days Completed (Exclude Sundays)
        # =========================================

        today = date.today()

        start_date = date(year, month, 1)

        # Current month
        if today.year == year and today.month == month:
            end_date = today

        # Old/Future month
        else:
            last_day = calendar.monthrange(year, month)[1]
            end_date = date(year, month, last_day)

        total_working_days = 0

        current_date = start_date

        while current_date <= end_date:

            # Sunday = 6
            if current_date.weekday() != 6:
                total_working_days += 1

            current_date += timedelta(days=1)

        # =========================================
        # Total Working Days From Master
        # =========================================

        month_master = ScheduleMonthMaster.objects.filter(
            month_no=str(month),
            year_no=str(year)
        ).first()

        total_month_days = (
            int(month_master.w_days)
            if month_master and month_master.w_days
            else 0
        )

        # =========================================
        # Remaining Days
        # =========================================

        days_rem = total_month_days - total_working_days

        # =========================================
        # Schedule Data
        # =========================================

        schedule_data = (
            ProductionSchedule.objects
            .filter(
                schedule_month__month_no=month,
                schedule_month__year_no=year
            )
            .values(
                'item_no',
                'item_code',
                'item_description'
            )
            .annotate(
                total_sch_qty=Coalesce(
                    Sum('sch_qty', output_field=IntegerField()),
                    Value(0)
                )
            )
            .order_by('item_no')
        )

        final_data = []

        # =========================================
        # Loop Data
        # =========================================

        for schedule in schedule_data:

            item_no = schedule['item_no']
            item_code = schedule['item_code']
            item_description = schedule['item_description']

            total_sch_qty = schedule['total_sch_qty'] or 0

            # =========================================
            # Invoice Qty
            # =========================================

            invoice_qty = (
                InvoiceItemdetails.objects
                .filter(
                    invoice__invoice_Date__month=month,
                    invoice__invoice_Date__year=year,
                    part_no=item_no,
                    part_code=item_code,
                    description=item_description
                )
                .aggregate(
                    total_inv_qty=Coalesce(
                        Sum('inv_qty'),
                        Value(0)
                    )
                )
            )

            total_inv_qty = invoice_qty['total_inv_qty'] or 0

            # =========================================
            # Balance Qty
            # =========================================

            bal_qty = int(total_sch_qty) - int(total_inv_qty)

            # =========================================
            # Current Average
            # =========================================

            if total_working_days > 0:
                cur_avg = round(
                    total_inv_qty / total_working_days,
                    2
                )
            else:
                cur_avg = 0

            # =========================================
            # Ask Rate
            # =========================================

            if days_rem > 0:
                ask_rate = round(
                    bal_qty / days_rem,
                    2
                )
            else:
                ask_rate = 0

            # =========================================
            # Status Percentage
            # =========================================

            if total_sch_qty > 0:
                status_percentage = round(
                    (total_inv_qty / total_sch_qty) * 100,
                    2
                )
            else:
                status_percentage = 0

            # =========================================
            # Final Response Data
            # =========================================

            final_data.append({

                "item_no": item_no,
                "item_code": item_code,
                "item_description": item_description,

                "W_Days": total_month_days,
                "Days_Comp": total_working_days,
                "Days_Rem": days_rem,

                "sch_qty": total_sch_qty,

                "total_inv_qty": total_inv_qty,

                "Cur_Avg": cur_avg,

                "bal_qty": bal_qty,

                "Ask_Rate": ask_rate,

                # New Field
                "status": f"{status_percentage}%"
            })

        return Response(
            {
                "message": "Month wise balance report fetched successfully",
                "month": month,
                "year": year,
                "data": final_data
            },
            status=status.HTTP_200_OK
        )
    



# class UpdateItemWiseMinMaxAPIView(APIView):
#     def get(self, request , pk=None):
#         queryset = UpdateItemWiseMinMax.objects.all().order_by('-id')
#         serializer = UpdateItemWiseMinMaxSerializer(queryset,many=True)
#         return Response(
#             {
#                 "message": "Data fetched successfully",
#                 "data": serializer.data
#             },
#             status=status.HTTP_200_OK
#         )

#     # ✅ POST API
#     def post(self, request):
#         serializer = UpdateItemWiseMinMaxSerializer(
#             data=request.data
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {
#                     "message": "Data created successfully",
#                     "data": serializer.data
#                 },
#                 status=status.HTTP_201_CREATED
#             )

#         return Response(
#             {
#                 "errors": serializer.errors
#             },
#             status=status.HTTP_400_BAD_REQUEST
#         )


#     # ✅ PUT API
#     def put(self, request, pk):
#         try:
#             instance = UpdateItemWiseMinMax.objects.get(id=pk)
#         except UpdateItemWiseMinMax.DoesNotExist:
#             return Response(
#                 {
#                     "error": "Data not found"
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = UpdateItemWiseMinMaxSerializer(
#             instance,
#             data=request.data
#         )

#         if serializer.is_valid():

#             serializer.save()

#             return Response(
#                 {
#                     "message": "Data updated successfully",
#                     "data": serializer.data
#                 },
#                 status=status.HTTP_200_OK
#             )

#         return Response(
#             {
#                 "errors": serializer.errors
#             },
#             status=status.HTTP_400_BAD_REQUEST
#         )


#     # ✅ DELETE API
#     def delete(self, request, pk):
#         try:
#             instance = UpdateItemWiseMinMax.objects.get(id=pk)
#         except UpdateItemWiseMinMax.DoesNotExist:
#             return Response(
#                 {
#                     "error": "Data not found"
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         instance.delete()
#         return Response(
#             {
#                 "message": "Data deleted successfully"
#             },
#             status=status.HTTP_200_OK
#         )
    




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from All_Masters.models import ItemTable
from .models import UpdateItemWiseMinMax

class UpdateItemWiseMinMaxAPIView(APIView):

    # ===================== GET =====================

    def get(self, request):

        main_group = request.GET.get("main_group")
        item_group = request.GET.get("item_group")
        item_search = request.GET.get("ItemSearch")

        items = ItemTable.objects.all()

        if main_group and main_group != "ALL":
            items = items.filter(main_group=main_group)

        if item_group and item_group != "ALL":
            items = items.filter(item_group=item_group)

        if item_search:
            items = items.filter(
                part_no__icontains=item_search
            )

        minmax_dict = {}

        latest_records = UpdateItemWiseMinMax.objects.order_by("-id")

        for obj in latest_records:
            if obj.item_no not in minmax_dict:
                minmax_dict[obj.item_no] = obj

        data = []

        for item in items:

            mm = minmax_dict.get(item.part_no)

            data.append({
                "id": mm.id if mm else None,
                "item_no": item.part_no,
                "item_code": item.Part_Code,
                "description": item.Name_Description,
                "item_groups": item.item_group,
                "main_groups": item.main_group,
                "unit": item.Unit_Code,
                "tariff_no": item.HSN_SAC_Code,
                "min_level": mm.min_level if mm else 0,
                "re_order_level": mm.re_order_level if mm else 0,
                "max_level": mm.max_level if mm else 0,
                "min_order": mm.min_order if mm else 0,
                "max_order": mm.max_order if mm else 0,
                "grn_tol_sub": mm.grn_tol_sub if mm else 0,
                "grn_tol_add": mm.grn_tol_add if mm else 0,
                "user": mm.user if mm else ""
            })

        return Response(
            {
                "message": "Data fetched successfully",
                "count": len(data),
                "data": data
            },
            status=status.HTTP_200_OK
        )

    # ===================== POST =====================

    def post(self, request):

        item_no = request.data.get("item_no")

        if not item_no:
            return Response(
                {
                    "message": "item_no is required"
                },
                status=400
            )

        latest_record = UpdateItemWiseMinMax.objects.filter(
            item_no=item_no
        ).order_by("-id").first()

        if latest_record:

            # old duplicate records delete
            UpdateItemWiseMinMax.objects.filter(
                item_no=item_no
            ).exclude(
                id=latest_record.id
            ).delete()

            serializer = UpdateItemWiseMinMaxSerializer(
                latest_record,
                data=request.data
            )

            message = "Data updated successfully"

        else:

            serializer = UpdateItemWiseMinMaxSerializer(
                data=request.data
            )

            message = "Data created successfully"

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": message,
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # ===================== DELETE =====================

    def delete(self, request, pk):

        try:
            obj = UpdateItemWiseMinMax.objects.get(id=pk)

        except UpdateItemWiseMinMax.DoesNotExist:

            return Response(
                {
                    "message": "Data not found"
                },
                status=404
            )

        obj.delete()

        return Response(
            {
                "message": "Deleted Successfully"
            }
        )

class DispatchPlanAPIView(APIView):

    # ✅ GET API
    def get(self, request , pk=None):
        queryset = DispatchPlan.objects.all().order_by('-id')
        serializer = DispatchPlanSerializer(queryset,many=True)
        return Response(
            {
                "message": "Data fetched successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


    # ✅ POST API
    def post(self, request):
        serializer = DispatchPlanSerializer( data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Data created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # ✅ PUT API
    def put(self, request, pk):
        try:
            instance = DispatchPlan.objects.get(id=pk)
        except DispatchPlan.DoesNotExist:
            return Response(
                {
                    "error": "Data not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = DispatchPlanSerializer(instance,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Data updated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


    #  DELETE API
    def delete(self, request, pk):
        try:
            instance = DispatchPlan.objects.get(id=pk)
        except DispatchPlan.DoesNotExist:
            return Response(
                {
                    "error": "Data not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        instance.delete()
        return Response(
            {
                "message": "Data deleted successfully"
            },
            status=status.HTTP_200_OK
        )
    


from All_Masters.models import Item
class CustomerItemListView(APIView):
    def get(self, request):
        customers = Item.objects.filter(type='Customer')
        serializer = ItemSerializer(customers, many=True)
        return Response({
            "message": "Customer type data fetched successfully",
            "count": customers.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    


from Sales.models import NewSalesOrder
from Sales.serializers import NewSalesOrderSerializer

class SalesOrderSearchAPIView(APIView):

    def get(self, request):

        customer = request.GET.get('customer')
        item_no = request.GET.get('item_no')
        item_code = request.GET.get('item_code')
        item_description = request.GET.get('item_description')

        queryset = NewSalesOrder.objects.all()

        # Customer filter
        if customer:
            queryset = queryset.filter(
                customer__icontains=customer
            )

        # Item No filter
        if item_no:
            queryset = queryset.filter(
                item__item_no__icontains=item_no
            )

        # Item Code filter
        if item_code:
            queryset = queryset.filter(
                item__item_code__icontains=item_code
            )

        # Item Description filter
        if item_description:
            queryset = queryset.filter(
                item__item_description__icontains=item_description
            )

        queryset = queryset.distinct().order_by('-id')

        serializer = NewSalesOrderSerializer(queryset, many=True)
        return Response(
            {
                "message": "Data fetched successfully",
                "count": queryset.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


from All_Masters.models import BOMItem,ItemTable
from Production.models import ProductionEntry
from django.db.models import Sum, F, Value, FloatField
from django.db.models.functions import Cast, Coalesce
from collections import defaultdict

def safe_float(value):
    try:
        return float(value)
    except:
        return 0
class LastOperationProdQtyAPI(APIView):

    def get(self, request):
        query = request.query_params.get("q", "").strip()
        if not query:
            return Response(
                {"error": 'Search query "q" is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        item = ItemTable.objects.filter(
            Q(Part_Code__icontains=query) |
            Q(part_no__icontains=query) |
            Q(Name_Description__icontains=query)
        ).first()

        if not item:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        bom_items = BOMItem.objects.filter(item=item)

        last_op_no = -1
        last_bom = None

        # 🔥 Find LAST OPNo
        for bom in bom_items:
            if not bom.OPNo:
                continue
            try:
                op_int = int(bom.OPNo.strip())
            except ValueError:
                continue

            if op_int > last_op_no:
                last_op_no = op_int
                last_bom = bom

        if not last_bom:
            return Response({"error": "No valid OP found"}, status=status.HTTP_404_NOT_FOUND)

        # 🔥 Get production entries for LAST OP
        prod_entries = ProductionEntry.objects.filter(
            item__icontains=item.Part_Code,
            operation__startswith=last_bom.OPNo
        )

        lot_map = defaultdict(float)
        total_prod_qty = 0.0

        for e in prod_entries:
            lot = (e.lot_no or "").split("|")[0].strip()
            qty = safe_float(e.prod_qty or 0)

            lot_map[lot] += qty
            total_prod_qty += qty

        lot_list = [
            {
                "lot_no": lot,
                "prod_qty": round(qty, 3)
            }
            for lot, qty in lot_map.items()
        ]

        return Response(
            {
                "last_operation": {
                    "part_code": item.Part_Code,
                    "part_no": item.part_no,
                    "Name_Description": item.Name_Description,
                    "OPNo": last_bom.OPNo,
                    "Operation": last_bom.Operation,
                    "prod_qty": round(total_prod_qty, 3),
                    "lots": lot_list
                }
            },
            status=status.HTTP_200_OK
        )

