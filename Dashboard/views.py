from django.shortcuts import render

# Create your views here.


from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from Sales.models import GstdetailsInvoice, SalesRateDiff
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from Sales.models import GstdetailsInvoice, SalesRateDiff

class AssessableValueReport(APIView):
    def get(self, request):
        month = request.query_params.get("month")
        year = request.query_params.get("year")

        # =========================
        # 🔹 Invoice Data
        # =========================
        invoice_data = GstdetailsInvoice.objects.select_related('invoice')

        if year:
            invoice_data = invoice_data.filter(invoice__invoice_Date__year=year)

        if month:
            invoice_data = invoice_data.filter(invoice__invoice_Date__month=month)

        gst_total = invoice_data.filter(
            invoice__items__invoice_type="GST"
        ).aggregate(total=Sum('assessble_value'))['total'] or 0

        scrap_total = invoice_data.filter(
            invoice__items__invoice_type="SCRAP"
        ).aggregate(total=Sum('assessble_value'))['total'] or 0

        # =========================
        # 🔹 Rate Diff Data
        # =========================
        rate_diff_data = SalesRateDiff.objects.all()

        if year:
            rate_diff_data = rate_diff_data.filter(debit_note_date__year=year)

        if month:
            rate_diff_data = rate_diff_data.filter(debit_note_date__month=month)

        rate_diff_total = rate_diff_data.aggregate(
            total=Sum('ass_amount')
        )['total'] or 0

        # =========================
        # 🔹 Grand Total
        # =========================
        grand_total = gst_total + scrap_total + rate_diff_total

        return Response({
            "month": month,
            "year": year,
            "GST_total_assessable_value": gst_total,
            "SCRAP_total_assessable_value": scrap_total,
            "RATE_DIFF_total_assessable_value": rate_diff_total,
            "GRAND_TOTAL": grand_total
        })
    

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from django.db.models.functions import TruncDate
import calendar
from datetime import date

class AssessableMonthlyReport(APIView):
    def get(self, request):
        year = int(request.GET.get('year'))
        month = int(request.GET.get('month'))

        # ✅ No TruncDate (Fix crash)
        queryset = (
            GstdetailsInvoice.objects
            .filter(
                invoice__invoice_Date__isnull=False,
                invoice__invoice_Date__year=year,
                invoice__invoice_Date__month=month
            )
            .values('invoice__invoice_Date')   # 👈 direct use
            .annotate(total_assessable=Sum('assessble_value'))
            .order_by('invoice__invoice_Date')
        )

        # Convert to dict
        data_dict = {
            str(item['invoice__invoice_Date']): item['total_assessable']
            for item in queryset
        }

        # Full month data
        import calendar
        from datetime import date

        total_days = calendar.monthrange(year, month)[1]

        result = []
        for day in range(1, total_days + 1):
            d = date(year, month, day)
            result.append({
                "date": str(d),
                "total_assessable": data_dict.get(str(d), 0)
            })

        return Response(result)
    

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, IntegerField
from django.db.models.functions import Cast, Coalesce
from django.db.models import Value
from Sales.models import InvoiceItemdetails

class TopCustomersReport(APIView):
    def get(self, request):

        queryset = (
            InvoiceItemdetails.objects
            .values('customer')
            .annotate(
                total_po_qty=Coalesce(
                    Sum(Cast('po_qty', IntegerField())), Value(0)
                ),
                total_assessable=Coalesce(
                    Sum('invoice__GSTdetails__assessble_value'), Value(0)
                )
            )
            .order_by('-total_po_qty')[:5]
        )
        return Response(queryset)
    



from django.db.models import Sum, IntegerField
from django.db.models.functions import Cast
from rest_framework.views import APIView
from rest_framework.response import Response

class CustomerDescriptionSummary(APIView):
    def get(self, request):
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')

        queryset = InvoiceItemdetails.objects.all()

        # ✅ Date filter
        if from_date and to_date:
            queryset = queryset.filter(date__range=[from_date, to_date])

        data = (
            queryset
            .values('customer', 'description')
            .annotate(
                total_po_qty=Sum(Cast('po_qty', IntegerField())),
                total_assessable_value=Sum('invoice__GSTdetails__assessble_value')
            )
        )

        return Response(data)
    

from datetime import date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, IntegerField, Value,Count
from django.db.models.functions import Coalesce
from Planning.models import ProductionSchedule

class BussinessSummaryAPIView(APIView):

    def get(self, request):

        month = request.query_params.get("month")
        year = request.query_params.get("year")

        if not month or not year:
            return Response(
                {"error": "month and year are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            month = int(month)
            year = int(year)
        except ValueError:
            return Response(
                {"error": "month and year must be integer"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Total Schedule Qty
        
        total_sch_qty = (            
            ProductionSchedule.objects
            .filter(
                schedule_month__month_no=month,
                schedule_month__year_no=year
            )
            .aggregate(
                total=Coalesce(
                    Sum("sch_qty", output_field=IntegerField()),
                    Value(0)
                )
            )["total"]
        )

        # Total Invoice Qty
        total_inv_qty = (
            
            InvoiceItemdetails.objects
            .filter(
                invoice__invoice_Date__month=month,
                invoice__invoice_Date__year=year
            )
            .aggregate(
                total=Coalesce(
                    Sum("inv_qty", output_field=IntegerField()),
                    Value(0)
                )
            )["total"]
        )

        bal_qty = total_sch_qty - total_inv_qty

        status_percentage = (
            round((total_inv_qty / total_sch_qty) * 100, 2)
            if total_sch_qty > 0 else 0
        )

        return Response(
            {
                "message": "Month wise summary fetched successfully",
                "month": month,
                "year": year,
                "total_sch_qty": total_sch_qty,
                "total_inv_qty": total_inv_qty,
                "bal_qty": bal_qty,
                "status": f"{status_percentage}%"
            },
            status=status.HTTP_200_OK
        )


# from django.db.models import Sum, IntegerField, Value
# from django.db.models.functions import Coalesce, Cast
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# class BussinessSummaryAPIView(APIView):

#     def get(self, request):

#         month = request.query_params.get("month")
#         year = request.query_params.get("year")

#         # ==========================
#         # Validation
#         # ==========================

#         if not month or not year:
#             return Response(
#                 {"error": "month and year are required"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         try:
#             month = int(month)
#             year = int(year)
#         except ValueError:
#             return Response(
#                 {"error": "month and year must be integer"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # ==========================
#         # Schedule Queryset
#         # ==========================

#         schedule_qs = ProductionSchedule.objects.filter(
#             schedule_month__month_no=month,
#             schedule_month__year_no=year
#         )

#         schedule_count = schedule_qs.count()

#         print("Schedule Count:", schedule_count)

#         # sch_qty is CharField, so cast to Integer
#         total_sch_qty = schedule_qs.aggregate(
#             total=Coalesce(
#                 Sum(
#                     Cast("sch_qty", IntegerField())
#                 ),
#                 Value(0)
#             )
#         )["total"]

#         # ==========================
#         # Invoice Queryset
#         # ==========================

#         invoice_qs = InvoiceItemdetails.objects.filter(
#             invoice__invoice_Date__month=month,
#             invoice__invoice_Date__year=year
#         )

#         invoice_count = invoice_qs.count()

#         print("Invoice Count:", invoice_count)

#         total_inv_qty = invoice_qs.aggregate(
#             total=Coalesce(
#                 Sum("inv_qty"),
#                 Value(0)
#             )
#         )["total"]

#         # ==========================
#         # Calculations
#         # ==========================

#         bal_qty = total_sch_qty - total_inv_qty

#         status_percentage = (
#             round((total_inv_qty / total_sch_qty) * 100, 2)
#             if total_sch_qty > 0 else 0
#         )

#         # ==========================
#         # Response
#         # ==========================

#         return Response(
#             {
#                 "message": "Month wise summary fetched successfully",
#                 "month": month,
#                 "year": year,

#                 # Debug Counts
#                 "schedule_count": schedule_count,
#                 "invoice_count": invoice_count,

#                 # Summary
#                 "total_sch_qty": total_sch_qty,
#                 "total_inv_qty": total_inv_qty,
#                 "bal_qty": bal_qty,
#                 "status": f"{status_percentage}%"
#             },
#             status=status.HTTP_200_OK
#         )

from collections import defaultdict

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from Sales.models import Invoice
from All_Masters.models import Item


class Top5RegionSalesAPIView(APIView):

    def get(self, request):
        try:
            region_summary = defaultdict(
                lambda: {
                    "assessable_value": 0,
                    "grand_total": 0
                }
            )

            invoices = Invoice.objects.prefetch_related(
                "GSTdetails"
            ).only(
                "id",
                "bill_to"
            )

            # Region Wise Data
            for invoice in invoices:

                if not invoice.bill_to:
                    continue

                try:
                    customer_name = invoice.bill_to.split("|")[0].strip()
                except Exception:
                    customer_name = invoice.bill_to.strip()

                customer = Item.objects.filter(
                    Name__iexact=customer_name,
                    type="Customer"
                ).only("Region").first()

                if not customer:
                    continue

                region = customer.Region or "Unknown"

                for gst in invoice.GSTdetails.all():
                    region_summary[region]["assessable_value"] += (
                        gst.assessble_value or 0
                    )
                    region_summary[region]["grand_total"] += (
                        gst.grand_total or 0
                    )

            # Total Assessable Value
            total_assessable_value = sum(
                row["assessable_value"]
                for row in region_summary.values()
            )

            # Format Response
            result = []

            for region, values in region_summary.items():

                percentage = 0

                if total_assessable_value > 0:
                    percentage = round(
                        (
                            values["assessable_value"]
                            / total_assessable_value
                        ) * 100,
                        2
                    )

                result.append({
                    "region": region,
                    "assessable_value": values["assessable_value"],
                    "grand_total": values["grand_total"],
                    "percentage": percentage
                })

            # Top 5 Regions
            result = sorted(
                result,
                key=lambda x: x["assessable_value"],
                reverse=True
            )[:5]

            return Response(
                {
                    "total_assessable_value": total_assessable_value,
                    "top_regions": result
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        


from django.db.models import Sum, Value, DecimalField
from Sales.models import NewSalesItemdetails

class BusinessSummaryValueAPIView(APIView):

    def get(self, request):
        month = request.query_params.get("month")
        year = request.query_params.get("year")

        if not month or not year:
            return Response(
                {"error": "month and year are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            month = int(month)
            year = int(year)
        except ValueError:
            return Response(
                {"error": "month and year must be integers"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Sales Order Assessable Value
        sales_order_assessable_value = (
            NewSalesItemdetails.objects
            .filter(
                newsaleoreder__so_date__month=month,
                newsaleoreder__so_date__year=year
            )
            .aggregate(
                total=Coalesce(
                    Sum("assessable_value"),
                    Value(0),
                    output_field=DecimalField()
                )
            )["total"]
        )

        # Invoice Assessable Value
        invoice_assessable_value = (
            GstdetailsInvoice.objects
            .filter(
                invoice__invoice_Date__month=month,
                invoice__invoice_Date__year=year
            )
            .aggregate(
                total=Coalesce(
                    Sum("assessble_value"),
                    Value(0),
                    output_field=DecimalField()
                )
            )["total"]
        )

        return Response(
            {
                "month": month,
                "year": year,
                "sales_order_assessable_value": sales_order_assessable_value,
                "invoice_assessable_value": invoice_assessable_value
            },
            status=status.HTTP_200_OK
        )
    



    """Purchase Dashboard APIs"""

# class PurchasePOSeriesSummaryAPIView(APIView):

#     def get(self, request):

#         # Example:
#         # /api/purchase-po-series-summary/?month=5&year=2026

#         month = request.GET.get("month")
#         year = request.GET.get("year")

#         purchase_orders = PurchasePO.objects.prefetch_related(
#             "Gst_Details"
#         )

#         # Filter by month and year
#         if month and year:
#             purchase_orders = purchase_orders.filter(
#                 PoDate__month=int(month),
#                 PoDate__year=int(year)
#             )
#         elif month:
#             purchase_orders = purchase_orders.filter(
#                 PoDate__month=int(month)
#             )
#         elif year:
#             purchase_orders = purchase_orders.filter(
#                 PoDate__year=int(year)
#             )

#         summary = defaultdict(lambda: {
#             "count": 0,
#             "assessable_value": Decimal("0.00")
#         })

#         total_count = 0
#         total_assessable_value = Decimal("0.00")

#         for po in purchase_orders:

#             if not po.PoDate:
#                 continue

#             series = po.Series if po.Series else "UNKNOWN"

#             ass_value = sum(
#                 gst.AssValue or Decimal("0.00")
#                 for gst in po.Gst_Details.all()
#             )

#             summary[series]["count"] += 1
#             summary[series]["assessable_value"] += ass_value

#             total_count += 1
#             total_assessable_value += ass_value

        
#         all_series = [
#             "RM",
#             "CONSUMABLE",
#             "SERVICE",
#             "ASSET",
#             "IMPORT"
#         ]

#         data = []

#         for series in all_series:
#             data.append({
#                 "series": series,
#                 "count": summary[series]["count"],
#                 "assessable_value": summary[series]["assessable_value"]
#             })

#         return Response({
#             "status": True,
#             "month": month,
#             "year": year,
#             "total_count": total_count,
#             "total_assessable_value": total_assessable_value,
#             "data": data
#         })
    

from decimal import Decimal
from collections import defaultdict

from rest_framework.views import APIView
from rest_framework.response import Response

from Purchase.models import PurchasePO, NewJobWorkPoInfo


class PurchasePOSeriesSummaryAPIView(APIView):

    def get(self, request):

        month = request.GET.get("month")
        year = request.GET.get("year")

        summary = defaultdict(lambda: {
            "count": 0,
            "assessable_value": Decimal("0.00")
        })

        total_count = 0
        total_assessable_value = Decimal("0.00")

        # ---------------- Purchase PO ---------------- #

        purchase_orders = PurchasePO.objects.prefetch_related(
            "Gst_Details"
        )

        if month and year:
            purchase_orders = purchase_orders.filter(
                PoDate__month=int(month),
                PoDate__year=int(year)
            )
        elif month:
            purchase_orders = purchase_orders.filter(
                PoDate__month=int(month)
            )
        elif year:
            purchase_orders = purchase_orders.filter(
                PoDate__year=int(year)
            )

        for po in purchase_orders:

            series = po.Series or "UNKNOWN"

            ass_value = sum(
                Decimal(str(gst.AssValue or 0))
                for gst in po.Gst_Details.all()
            )

            summary[series]["count"] += 1
            summary[series]["assessable_value"] += ass_value

            total_count += 1
            total_assessable_value += ass_value

        # ---------------- Job Work PO ---------------- #

        
        jobwork = NewJobWorkPoInfo.objects.all()

        if month and year:
            month = str(month).zfill(2)  # 5 -> 05
            jobwork = jobwork.filter(
                PoDate__startswith=f"{year}-{month}"
            )

        elif year:
            jobwork = jobwork.filter(
                PoDate__startswith=str(year)
            )


        for po in jobwork:

            series = po.Series or "JOBWORK"

            try:
                ass_value = Decimal(str(po.TOC_AssableValue or 0))
            except:
                ass_value = Decimal("0.00")

            summary[series]["count"] += 1
            summary[series]["assessable_value"] += ass_value

            total_count += 1
            total_assessable_value += ass_value

        all_series = [
            "RM",
            "CONSUMABLE",
            "SERVICE",
            "ASSET",
            "IMPORT",
            "JOBWORK",
        ]

        data = []

        for series in all_series:
            data.append({
                "series": series,
                "count": summary[series]["count"],
                "assessable_value": summary[series]["assessable_value"]
            })

        return Response({
            "status": True,
            "month": month,
            "year": year,
            "total_count": total_count,
            "total_assessable_value": total_assessable_value,
            "data": data
        })



from datetime import datetime
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from Store.models import GrnGst

class FinancialYearGrnTotalAPIView(APIView):

    def get(self, request):
        year = int(request.GET.get("year", datetime.now().year))

        financial_months = [
            ("April", 4, year),
            ("May", 5, year),
            ("June", 6, year),
            ("July", 7, year),
            ("August", 8, year),
            ("September", 9, year),
            ("October", 10, year),
            ("November", 11, year),
            ("December", 12, year),
            ("January", 1, year + 1),
            ("February", 2, year + 1),
            ("March", 3, year + 1),
        ]

        result = []

        for month_name, month, y in financial_months:

            start_date = f"{y}-{month:02d}-01"

            if month == 12:
                end_date = f"{y+1}-01-01"
            else:
                end_date = f"{y}-{month+1:02d}-01"

            total = (
                GrnGst.objects.filter(
                    New_MRN_Detail__GrnDate__gte=start_date,
                    New_MRN_Detail__GrnDate__lt=end_date,
                ).aggregate(
                    total_amount=Sum("total")
                )["total_amount"] or 0
            )

            result.append({
                "month": month_name,
                "year": y,
                "total": total
            })

        return Response({
            "financial_year": f"{year}-{year+1}",
            "data": result
        })


from calendar import monthrange
class MonthlyGrnTotalAPIView(APIView):

    def get(self, request):

        month = int(request.GET.get("month"))
        year = int(request.GET.get("year"))

        days_in_month = monthrange(year, month)[1]

        data = []

        for day in range(1, days_in_month + 1):

            date = f"{year}-{month:02d}-{day:02d}"

            total = (
                GrnGst.objects.filter(
                    New_MRN_Detail__GrnDate=date
                ).values_list("total", flat=True)
            )

            day_total = sum(
                Decimal(value or 0)
                for value in total
            )

            data.append({
                "date": date,
                "day": day,
                "total": day_total
            })

        return Response({
            "month": month,
            "year": year,
            "data": data
        })
    

from decimal import Decimal
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from Store.models import GrnGenralDetail



class TopFiveSupplierAPIView(APIView):

    def get(self, request):

        # Overall purchase total
        overall_total = (
            GrnGenralDetail.objects.aggregate(
                total=Sum("GrnGst__total")
            )["total"] or Decimal("0.00")
        )

        # Top 5 suppliers
        suppliers = (
            GrnGenralDetail.objects
            .values("SelectSupplier")
            .annotate(
                total_amount=Sum("GrnGst__total"),
                total_grn_qty=Sum("NewGrnList__GrnQty")
            )
            .order_by("-total_amount")[:5]
        )

        data = []

        for supplier in suppliers:

            total = supplier["total_amount"] or Decimal("0.00")
            grn_qty = supplier["total_grn_qty"] or Decimal("0.00")

            percentage = (
                round((total / overall_total) * 100, 2)
                if overall_total > 0 else 0
            )

            data.append({
                "supplier": supplier["SelectSupplier"],
                "grn_qty": grn_qty,
                "total": total,
                "percentage": percentage
            })

        return Response({
            "status": True,
            "overall_total": overall_total,
            "count": len(data),
            "data": data
        })


from decimal import Decimal

from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response

from All_Masters.models import ItemTable
from Store.models import NewGrnList

class ItemWiseGrnReportAPIView(APIView):

    def get(self, request):

        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")
        part_no = request.GET.get("part_no")   # Optional

        queryset = NewGrnList.objects.filter(
            New_MRN_Detail__GrnDate__gte=from_date,
            New_MRN_Detail__GrnDate__lte=to_date
        )

        # Particular Part Filter
        if part_no:
            queryset = queryset.filter(ItemNoCode=part_no)

        item_data = (
            queryset.values("ItemNoCode")
            .annotate(
                total_grn_qty=Sum("GrnQty")
            )
            .order_by("ItemNoCode")
        )

        response_data = []

        for item in item_data:

            item_code = item["ItemNoCode"]

            item_master = ItemTable.objects.filter(
                part_no=item_code
            ).first()

            ass_value = (
                GrnGst.objects.filter(
                    ItemCode=item_code,
                    New_MRN_Detail__GrnDate__gte=from_date,
                    New_MRN_Detail__GrnDate__lte=to_date
                ).aggregate(
                    total_ass_value=Sum("AssValue")
                )["total_ass_value"] or Decimal("0.00")
            )

            response_data.append({
                "part_no": item_master.part_no if item_master else item_code,
                "Part_Code": item_master.Part_Code if item_master else "",
                "Name_Description": item_master.Name_Description if item_master else "",
                "main_group": item_master.main_group if item_master else "",
                "item_group": item_master.item_group if item_master else "",
                "total_grn_qty": item["total_grn_qty"] or 0,
                "total_ass_value": ass_value
            })

        return Response({
            "status": True,
            "count": len(response_data),
            "data": response_data
        })
    


class MainGroupWiseGrnReportAPIView(APIView):

    def get(self, request):

        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")

        result = {}

        # GRN Qty
        grn_items = NewGrnList.objects.filter(
            New_MRN_Detail__GrnDate__gte=from_date,
            New_MRN_Detail__GrnDate__lte=to_date
        )

        for item in grn_items:

            item_master = ItemTable.objects.filter(
                part_no=item.ItemNoCode
            ).first()

            if not item_master:
                continue

            group = item_master.main_group

            if group not in result:
                result[group] = {
                    "main_group": group,
                    "total_grn_qty": Decimal("0.00"),
                    "total_ass_value": Decimal("0.00"),
                }

            result[group]["total_grn_qty"] += item.GrnQty or Decimal("0.00")

        # AssValue
        gst_items = GrnGst.objects.filter(
            New_MRN_Detail__GrnDate__gte=from_date,
            New_MRN_Detail__GrnDate__lte=to_date
        )

        for gst in gst_items:

            item_master = ItemTable.objects.filter(
                part_no=gst.ItemCode
            ).first()

            if not item_master:
                continue

            group = item_master.main_group

            if group not in result:
                result[group] = {
                    "main_group": group,
                    "total_grn_qty": Decimal("0.00"),
                    "total_ass_value": Decimal("0.00"),
                }

            result[group]["total_ass_value"] += Decimal(
                gst.AssValue or 0
            )

        return Response({
            "status": True,
            "count": len(result),
            "data": list(result.values())
        })
    





# PPC

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Value, IntegerField
from django.db.models.functions import Coalesce

class MonthWiseScheduleQtyAPIView(APIView):

    def get(self, request):

        month = request.query_params.get("month")
        year = request.query_params.get("year")

        if not month or not year:
            return Response(
                {"error": "month and year are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            month = int(month)
            year = int(year)
        except ValueError:
            return Response(
                {"error": "month and year must be integer"},
                status=status.HTTP_400_BAD_REQUEST
            )

        total_sch_qty = (
            ProductionSchedule.objects
            .filter(
                schedule_month__month_no=month,
                schedule_month__year_no=year
            )
            .aggregate(
                total_sch_qty=Coalesce(
                    Sum("sch_qty"),
                    Value(0),
                    output_field=IntegerField()
                )
            )
        )

        return Response(
            {
                "month": month,
                "year": year,
                "total_sch_qty": total_sch_qty["total_sch_qty"]
            },
            status=status.HTTP_200_OK
        )





# Store 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
 
from Store.models import InwardChallan2,GrnGenralDetail
from Sales.models import Newgstsalesreturn

class InwardMonthlyEntryAPIView(APIView):

    def get(self, request):

        month = request.GET.get("month")
        year = request.GET.get("year")

        if not month or not year:
            return Response(
                {"error": "month and year are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        month = f"{int(month):02d}"   # 5 -> 05

        date_prefix = f"{year}-{month}"

        # Sales Return (DateField)
        sales_return_count = Newgstsalesreturn.objects.filter(
            sales_return_date__year=year,
            sales_return_date__month=int(month)
        ).count()

        # Inward Challan (CharField)
        inward_challan_count = InwardChallan2.objects.filter(
            InwardDate__startswith=date_prefix
        ).count()

        # GRN (CharField)
        grn_count = GrnGenralDetail.objects.filter(
            GrnDate__startswith=date_prefix
        ).count()

        return Response({
            "month": int(month),
            "year": int(year),
            "sales_return_entries": sales_return_count,
            "inward_challan_entries": inward_challan_count,
            "grn_entries": grn_count,
            "total_entries": (
                sales_return_count +
                inward_challan_count +
                grn_count
            )
        })
    


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from Sales.models import Invoice,onwardchallan
from Store.models import MaterialChallan


class OutwardMonthlyEntryAPIView(APIView):

    def get(self, request):

        month = request.GET.get("month")
        year = request.GET.get("year")

        if not month or not year:
            return Response(
                {"error": "month and year are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            month = int(month)
            year = int(year)
        except ValueError:
            return Response(
                {"error": "month and year must be integers"},
                status=status.HTTP_400_BAD_REQUEST
            )

        month_str = f"{month:02d}"
        prefix = f"{year}-{month_str}"

        # Invoice (DateField)
        invoice_count = Invoice.objects.filter(
            invoice_Date__year=year,
            invoice_Date__month=month
        ).count()

        # Onward Challan (DateField)
        onward_challan_count = onwardchallan.objects.filter(
            challan_date__year=year,
            challan_date__month=month
        ).count()

        # Material Issue (CharField -> YYYY-MM-DD)
        material_issue_count = MaterialChallan.objects.filter(
            MaterialIssueDate__startswith=prefix
        ).count()

        return Response({
            "month": month,
            "year": year,
            "invoice_entries": invoice_count,
            "onward_challan_entries": onward_challan_count,
            "material_issue_entries": material_issue_count,
            "total_entries": (
                invoice_count +
                onward_challan_count +
                material_issue_count
            )
        })
    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from Planning.models import UpdateItemWiseMinMax


class UpdateItemWiseMinMaxAPIView(APIView):

    def get(self, request):

        queryset = UpdateItemWiseMinMax.objects.all().order_by("item_no")

        data = []

        for obj in queryset:
            data.append({
                "id": obj.id,
                "item_no": obj.item_no,
                "item_code": obj.item_code,
                "description": obj.description,
                "item_groups": obj.item_groups,
                "main_groups": obj.main_groups,
                "unit": obj.unit,
                "tariff_no": obj.tariff_no,
                "min_level": obj.min_level,
                "re_order_level": obj.re_order_level,
                "max_level": obj.max_level,
                "min_order": obj.min_order,
                "max_order": obj.max_order,
                "grn_tol_sub": obj.grn_tol_sub,
                "grn_tol_add": obj.grn_tol_add,
                "user": obj.user,
            })

        return Response(
            {
                "status": True,
                "count": queryset.count(),
                "data": data,
            },
            status=status.HTTP_200_OK,
        )


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from Sales.models import NewSalesItemdetails


class FGItemListAPIView(APIView):

    def get(self, request):

        items = (
            NewSalesItemdetails.objects
            .filter(item_no__startswith="FG")
            .values(
                "item_no",
                "item_code",
                "item_description",
                "uom",
                "hsn_code",
                "rate"
            )
            .distinct()
            .order_by("item_no")
        )

        data = []

        for item in items:
            data.append({
                "item_no": item.get("item_no") or "",
                "item_code": item.get("item_code") or "",
                "description": item.get("item_description") or "",
                "item_groups": "FG",
                "main_groups": "FG",
                "unit": item.get("uom") or "",
                "tariff_no/hsn_code": item.get("hsn_code") or "",
                "min_level": 0,
                "re_order_level": 0,
                "max_level": 0,
                "rate": item.get("rate") or 0,
            })

        return Response(
            {
                "status": True,
                "count": len(data),
                "data": data,
            },
            status=status.HTTP_200_OK,
        )
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from Planning.models import UpdateItemWiseMinMax
from Sales.models import NewSalesItemdetails


# class ItemMasterAPIView(APIView):

#     def get(self, request):

#         data = []

#         # Existing Item Master Data
#         queryset = UpdateItemWiseMinMax.objects.all().order_by("item_no")

#         for obj in queryset:
#             data.append({
#                 "id": obj.id,
#                 "item_no": obj.item_no,
#                 "item_code": obj.item_code,
#                 "description": obj.description,
#                 "item_groups": obj.item_groups,
#                 "main_groups": obj.main_groups,
#                 "unit": obj.unit,
#                 "tariff_no": obj.tariff_no,
#                 "min_level": obj.min_level,
#                 "re_order_level": obj.re_order_level,
#                 "max_level": obj.max_level,
#                 "min_order": obj.min_order,
#                 "max_order": obj.max_order,
#                 "grn_tol_sub": obj.grn_tol_sub,
#                 "grn_tol_add": obj.grn_tol_add,
#                 "rate": 0,
#                 "user": obj.user,
#             })

#         # Existing item numbers to avoid duplicates
#         existing_item_nos = set(
#             UpdateItemWiseMinMax.objects.values_list("item_no", flat=True)
#         )

#         # FG Items
#         fg_items = (
#             NewSalesItemdetails.objects
#             .filter(item_no__startswith="FG")
#             .values(
#                 "item_no",
#                 "item_code",
#                 "item_description",
#                 "uom",
#                 "hsn_code",
#                 "rate",
#             )
#             .distinct()
#             .order_by("item_no")
#         )

#         for item in fg_items:

#             if item["item_no"] in existing_item_nos:
#                 continue

#             data.append({
#                 "id": None,
#                 "item_no": item.get("item_no") or "",
#                 "item_code": item.get("item_code") or "",
#                 "description": item.get("item_description") or "",
#                 "item_groups": "FG",
#                 "main_groups": "FG",
#                 "unit": item.get("uom") or "",
#                 "tariff_no": item.get("hsn_code") or "",
#                 "min_level": 0,
#                 "re_order_level": 0,
#                 "max_level": 0,
#                 "min_order": 0,
#                 "max_order": 0,
#                 "grn_tol_sub": 0,
#                 "grn_tol_add": 0,
#                 "rate": item.get("rate") or 0,
#                 "user": "",
#             })

#         return Response(
#             {
#                 "status": True,
#                 "count": len(data),
#                 "data": data,
#             },
#             status=status.HTTP_200_OK,
#         )


from collections import defaultdict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from Planning.models import UpdateItemWiseMinMax
from Sales.models import NewSalesItemdetails
from All_Masters.models import BOMItem
from Production.models import ProductionEntry


class ItemMasterAPIView(APIView):

    def get(self, request):

        data = []

        # -------------------------------
        # Calculate Stock for all items
        # -------------------------------
        stock_dict = {}

        item_list = (
            BOMItem.objects.values_list("item__Part_Code", flat=True)
            .distinct()
        )

        for part_no in item_list:

            bom_qs = BOMItem.objects.filter(
                item__Part_Code=part_no
            )

            if not bom_qs.exists():
                continue

            finish_bom = bom_qs.filter(Operation__icontains="FINISH")

            if finish_bom.exists():
                final_bom = finish_bom.first()
            else:
                final_bom = max(
                    bom_qs,
                    key=lambda x: int(x.OPNo) if str(x.OPNo).isdigit() else 0
                )

            final_opno = str(final_bom.OPNo).strip()

            total_qty = (
                ProductionEntry.objects.filter(
                    item__icontains=part_no,
                    operation__startswith=final_opno
                )
                .aggregate(total=Sum("prod_qty"))
            )["total"] or 0

            stock_dict[part_no] = round(total_qty, 2)

        # ---------------------------------
        # Existing Item Master Data
        # ---------------------------------

        queryset = UpdateItemWiseMinMax.objects.all().order_by("item_no")

        for obj in queryset:

            stock = stock_dict.get(obj.item_code, 0)

            data.append({
                "id": obj.id,
                "item_no": obj.item_no,
                "item_code": obj.item_code,
                "description": obj.description,
                "item_groups": obj.item_groups,
                "main_groups": obj.main_groups,
                "unit": obj.unit,
                "tariff_no": obj.tariff_no,
                "min_level": obj.min_level,
                "re_order_level": obj.re_order_level,
                "max_level": obj.max_level,
                "min_order": obj.min_order,
                "max_order": obj.max_order,
                "grn_tol_sub": obj.grn_tol_sub,
                "grn_tol_add": obj.grn_tol_add,
                "rate": 0,
                "stock": stock,
                "user": obj.user,
            })

        existing_item_nos = set(
            UpdateItemWiseMinMax.objects.values_list(
                "item_no",
                flat=True
            )
        )

        fg_items = (
            NewSalesItemdetails.objects
            .filter(item_no__startswith="FG")
            .values(
                "item_no",
                "item_code",
                "item_description",
                "uom",
                "hsn_code",
                "rate",
            )
            .distinct()
            .order_by("item_no")
        )

        for item in fg_items:

            if item["item_no"] in existing_item_nos:
                continue

            stock = stock_dict.get(item.get("item_code"), 0)

            data.append({
                "id": None,
                "item_no": item.get("item_no") or "",
                "item_code": item.get("item_code") or "",
                "description": item.get("item_description") or "",
                "item_groups": "FG",
                "main_groups": "FG",
                "unit": item.get("uom") or "",
                "tariff_no": item.get("hsn_code") or "",
                "min_level": 0,
                "re_order_level": 0,
                "max_level": 0,
                "min_order": 0,
                "max_order": 0,
                "grn_tol_sub": 0,
                "grn_tol_add": 0,
                "rate": item.get("rate") or 0,
                "stock": stock,
                "user": "",
            })

        return Response(
            {
                "status": True,
                "count": len(data),
                "data": data,
            },
            status=status.HTTP_200_OK,
        )
    

from rest_framework.views import APIView
from rest_framework.response import Response
from Production.models import ProductionEntry


# class ProductionReworkReportAPIView(APIView):

#     def get(self, request):

#         queryset = ProductionEntry.objects.all().order_by("-id")

#         data = []

#         for obj in queryset:

#             # Item parsing
#             item_no = ""
#             item_code = ""
#             item_description = ""

#             if obj.item:
#                 item_parts = [x.strip() for x in obj.item.split("|")]

#                 if len(item_parts) >= 3:
#                     item_no = item_parts[0]
#                     item_code = item_parts[1]
#                     item_description = item_parts[2]

#             # Operation parsing
#             part_no = ""
#             operation_no = ""

#             if obj.operation:
#                 op_parts = [x.strip() for x in obj.operation.split("|")]

#                 if len(op_parts) >= 2:
#                     operation_no = op_parts[0]
#                     part_no = op_parts[1]

#             # Qty conversion
#             try:
#                 prod_qty = float(obj.prod_qty or 0)
#             except:
#                 prod_qty = 0

#             try:
#                 rework_qty = float(obj.rework_qty or 0)
#             except:
#                 rework_qty = 0

#             # Percentage
#             percentage = 0
#             if prod_qty > 0:
#                 percentage = round((rework_qty * 100) / prod_qty, 2)

#             data.append({
#                 "id": obj.id,
#                 "item_no": item_no,
#                 "item_code": item_code,
#                 "item_description": item_description,
#                 "part_no": part_no,
#                 "operation": operation_no,
#                 "prod_qty": prod_qty,
#                 "rework_qty": rework_qty,
#                 "percentage": percentage,
#             })

#         return Response(data)


from rest_framework.views import APIView
from rest_framework.response import Response
from Production.models import ProductionEntry


class ProductionReworkReportAPIView(APIView):

    def get(self, request):

        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")

        queryset = ProductionEntry.objects.all().order_by("-id")

        if from_date:
            queryset = queryset.filter(Date__gte=from_date)

        if to_date:
            queryset = queryset.filter(Date__lte=to_date)

        data = []

        for obj in queryset:

            # Parse item field
            item_no = ""
            item_code = ""
            item_description = ""

            if obj.item:
                item_parts = [i.strip() for i in obj.item.split("|")]
                if len(item_parts) >= 3:
                    item_no = item_parts[0]
                    item_code = item_parts[1]
                    item_description = item_parts[2]

            # Parse operation field
            operation = ""
            part_no = ""

            if obj.operation:
                op_parts = [i.strip() for i in obj.operation.split("|")]
                if len(op_parts) >= 2:
                    operation = op_parts[0]
                    part_no = op_parts[1]

            # Convert quantities
            try:
                prod_qty = float(obj.prod_qty or 0)
            except (ValueError, TypeError):
                prod_qty = 0

            try:
                rework_qty = float(obj.rework_qty or 0)
            except (ValueError, TypeError):
                rework_qty = 0

            # Calculate percentage
            percentage = round((rework_qty * 100 / prod_qty), 2) if prod_qty else 0

            data.append({
                "id": obj.id,
                "date": obj.Date,
                "item_no": item_no,
                "item_code": item_code,
                "item_description": item_description,
                "operation": operation,
                "part_no": part_no,
                "prod_qty": prod_qty,
                "rework_qty": rework_qty,
                "percentage": percentage,
            })

        return Response(data)
    

from rest_framework.views import APIView
from rest_framework.response import Response
from Production.models import ProductionEntry


class ProductionRejectReportAPIView(APIView):

    def get(self, request):

        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")

        queryset = ProductionEntry.objects.all().order_by("-id")

        if from_date:
            queryset = queryset.filter(Date__gte=from_date)

        if to_date:
            queryset = queryset.filter(Date__lte=to_date)

        data = []

        for obj in queryset:

            # Parse item
            item_no = ""
            item_code = ""
            item_description = ""

            if obj.item:
                item_parts = [i.strip() for i in obj.item.split("|")]

                if len(item_parts) >= 3:
                    item_no = item_parts[0]
                    item_code = item_parts[1]
                    item_description = item_parts[2]

            # Parse operation
            operation = ""
            part_no = ""

            if obj.operation:
                op_parts = [i.strip() for i in obj.operation.split("|")]

                if len(op_parts) >= 2:
                    operation = op_parts[0]
                    part_no = op_parts[1]

            # Convert quantities
            try:
                prod_qty = float(obj.prod_qty or 0)
            except (ValueError, TypeError):
                prod_qty = 0

            try:
                reject_qty = float(obj.reject_qty or 0)
            except (ValueError, TypeError):
                reject_qty = 0

            # Calculate reject percentage
            percentage = 0
            if prod_qty > 0:
                percentage = round((reject_qty * 100) / prod_qty, 2)

            data.append({
                "id": obj.id,
                "date": obj.Date,
                "item_no": item_no,
                "item_code": item_code,
                "item_description": item_description,
                "operation": operation,
                "part_no": part_no,
                "prod_qty": prod_qty,
                "reject_qty": reject_qty,
                "percentage": percentage,
            })

        return Response(data)



from datetime import datetime, timedelta
from collections import defaultdict

from rest_framework.views import APIView
from rest_framework.response import Response
from Production.models import ProductionEntry


class ProductionRejectMonthWiseAPIView(APIView):

    def get(self, request):

        year = request.GET.get("year")
        month = request.GET.get("month")

        if not year or not month:
            return Response({
                "error": "year and month are required"
            }, status=400)

        month = int(month)
        year = int(year)

        start_date = datetime(year, month, 1).date()

        if month == 12:
            end_date = datetime(year + 1, 1, 1).date() - timedelta(days=1)
        else:
            end_date = datetime(year, month + 1, 1).date() - timedelta(days=1)

        queryset = ProductionEntry.objects.filter(
            Date__gte=str(start_date),
            Date__lte=str(end_date)
        )

        reject_data = defaultdict(float)

        for obj in queryset:
            try:
                qty = float(obj.reject_qty or 0)
            except (ValueError, TypeError):
                qty = 0

            reject_data[obj.Date] += qty

        result = []

        current = start_date

        while current <= end_date:
            date_str = current.strftime("%Y-%m-%d")

            result.append({
                "date": date_str,
                "reject_qty": reject_data.get(date_str, 0)
            })

            current += timedelta(days=1)

        return Response(result)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from Production.models import ScrapLineRejectionNote

class ScrapRejectMonthTotalAPIView(APIView):

    def get(self, request):

        year = request.GET.get("year")
        month = request.GET.get("month")

        if not year or not month:
            return Response(
                {"error": "year and month are required"},
                status=400
            )

        month_str = f"{int(year):04d}-{int(month):02d}"

        queryset = ScrapLineRejectionNote.objects.filter(
            ScrapRejectionNoteDate__startswith=month_str
        )

        total_qty = 0
        remarks = []

        for obj in queryset:

            for item in obj.scrap_items.all():
                try:
                    total_qty += float(item.ScrapRejectionQty or 0)
                except (ValueError, TypeError):
                    pass

            if obj.ScrapRejectRemark:
                remarks.append(obj.ScrapRejectRemark)

        return Response({
            "month": month_str,
            "total_scrap_rej_qty": total_qty,
            "remark": ", ".join(set(remarks))
        })
    

from decimal import Decimal
from collections import OrderedDict

from rest_framework.views import APIView
from rest_framework.response import Response

from Sales.models import Newgstsalesreturn


class SalesReturnFinancialYearAPIView(APIView):

    def get(self, request):

        financial_year = request.GET.get("financial_year")

        if not financial_year:
            return Response(
                {"error": "financial_year is required. Example: 2025-2026"},
                status=400
            )

        try:
            start_year = int(financial_year.split("-")[0])
            end_year = int(financial_year.split("-")[1])
        except:
            return Response(
                {"error": "Invalid financial_year format. Example: 2025-2026"},
                status=400
            )

        months = OrderedDict([
            (4, "April"),
            (5, "May"),
            (6, "June"),
            (7, "July"),
            (8, "August"),
            (9, "September"),
            (10, "October"),
            (11, "November"),
            (12, "December"),
            (1, "January"),
            (2, "February"),
            (3, "March"),
        ])

        result = []

        for month_no, month_name in months.items():

            if month_no >= 4:
                year = start_year
            else:
                year = end_year

            sales = Newgstsalesreturn.objects.filter(
                sales_return_date__year=year,
                sales_return_date__month=month_no
            )

            grand_total = Decimal("0")
            return_qty = Decimal("0")

            customer_set = set()
            item_count = 0

            for sale in sales:

                if sale.cust_name:
                    customer_set.add(sale.cust_name)

                items = sale.items.all()

                item_count += items.count()

                for item in items:
                    grand_total += item.grand_total or Decimal("0")
                    return_qty += item.return_qty or Decimal("0")

            result.append({
                "month": month_name,
                "grand_total": float(grand_total),
                "return_qty": float(return_qty),
                "customer_count": len(customer_set),
                "item_count": item_count,
            })

        return Response(result)