from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

from .models import *
from .serializers import *


from Sales.models import Invoice
from Sales.serializers import InvoiceSerializer
class InvoiceDateFilterAPIView(APIView):
    def get(self, request):
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')

        if not from_date or not to_date:
            return Response(
                {
                    "status": False,
                    "message": "from_date and to_date are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
            to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {
                    "status": False,
                    "message": "Date format should be YYYY-MM-DD"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        invoices = Invoice.objects.filter(
            invoice_Date__range=[from_date, to_date]
        ).order_by('-invoice_Date')

        serializer = InvoiceSerializer(invoices, many=True)

        return Response(
            {
                "status": True,
                "count": invoices.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


# class PurchasePODateFilterAPIView(APIView):

#     def get(self, request):

#         from_date = request.GET.get('from_date')
#         to_date = request.GET.get('to_date')

#         queryset = PurchasePO.objects.all().order_by('-id')

#         # ✅ Date Filter
#         if from_date and to_date:
#             try:
#                 from_date = datetime.strptime(
#                     from_date,
#                     "%Y-%m-%d"
#                 ).date()

#                 to_date = datetime.strptime(
#                     to_date,
#                     "%Y-%m-%d"
#                 ).date()

#                 queryset = queryset.filter(
#                     PoDate__range=[from_date, to_date]
#                 )

#             except ValueError:
#                 return Response(
#                     {
#                         "message": "Invalid date format. Use YYYY-MM-DD"
#                     },
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#         # ✅ Existing Bill Register PO + ItemCode
#         existing_pairs = set(
#             BillRegisterItem.objects.values_list(
#                 'po_no',
#                 'item_code'
#             )
#         )

#         final_data = []

#         for po in queryset:

#             # ✅ Correct ManyToMany field
#             po_items = po.Item_Detail_Enter.all()

#             filtered_items = []

#             for item in po_items:

#                 pair = (po.PoNo, item.Item)

#                 # ✅ Agar bill register me nahi hai
#                 if pair not in existing_pairs:

#                     filtered_items.append({
#                         "id": item.id,
#                         "Item": item.Item,
#                         "ItemDescription": item.ItemDescription,
#                         "ItemSize": item.ItemSize,
#                         "Rate": item.Rate,
#                         "Disc": item.Disc,
#                         "Qty": item.Qty,
#                         "Unit": item.Unit,
#                         "Particular": item.Particular,
#                         "Mill_Name": item.Mill_Name,
#                         "DeliveryDt": item.DeliveryDt,
#                     })

#             # ✅ Agar items bache hain tabhi PO show karo
#             if filtered_items:

#                 po_data = PurchasePOSerializer(po).data

#                 # overwrite item details
#                 po_data["item_details"] = filtered_items

#                 final_data.append(po_data)

#         return Response(
#             {
#                 "message": "Data fetched successfully",
#                 "count": len(final_data),
#                 "data": final_data
#             },
#             status=status.HTTP_200_OK
#         )


from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Store.models import GrnGenralDetail
from Store.serializers import GrnGenralDetailSerializer

class GrnDateFilterAPIView(APIView):

    def get(self, request):

        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')

        queryset = GrnGenralDetail.objects.all().order_by('-id')

        # ✅ GRN Date Filter
        if from_date and to_date:
            try:
                from_date = datetime.strptime(
                    from_date,
                    "%Y-%m-%d"
                ).date()

                to_date = datetime.strptime(
                    to_date,
                    "%Y-%m-%d"
                ).date()

                queryset = queryset.filter(
                    GrnDate__range=[from_date, to_date]
                )

            except ValueError:
                return Response(
                    {
                        "message": "Invalid date format. Use YYYY-MM-DD"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        # ✅ Existing Bill Register PO + ItemCode
        existing_pairs = set(
            BillRegisterItem.objects.values_list(
                'po_no',
                'item_code'
            )
        )

        final_data = []

        for grn in queryset:

            # ✅ GRN Item Filter
            filtered_items = []

            grn_items = grn.NewGrnList.all()

            for item in grn_items:

                pair = (item.PoNo, item.ItemNoCode)

                # ✅ Agar Bill Register me nahi hai
                if pair not in existing_pairs:

                    filtered_items.append({
                        "id": item.id,
                        "PoNo": item.PoNo,
                        "Date": item.Date,
                        "ItemNoCode": item.ItemNoCode,
                        "Description": item.Description,
                        "Rate": item.Rate,
                        "PoQty": item.PoQty,
                        "BalQty": item.BalQty,
                        "ChalQty": item.ChalQty,
                        "GrnQty": item.GrnQty,
                        "ShortExcessQty": item.ShortExcessQty,
                        "UnitCode": item.UnitCode,
                        "Total": item.Total,
                        "HeatNo": item.HeatNo,
                        "MfgDate": item.MfgDate,
                    })

            # ✅ Agar filtered items hai tabhi GRN show karo
            if filtered_items:

                grn_data = GrnGenralDetailSerializer(grn).data

                # overwrite item list
                grn_data["NewGrnList"] = filtered_items

                final_data.append(grn_data)

        return Response(
            {
                "message": "Data fetched successfully",
                "count": len(final_data),
                "data": final_data
            },
            status=status.HTTP_200_OK
        )







class PendingBillGrnlistAPIView(APIView):
    # GET ALL DATA
    def get(self, request):
        queryset = PendingBillGrnlist.objects.all().order_by('-id')
        serializer = PendingBillGrnlistSerializer(queryset, many=True)

        return Response({
            "message": "Data fetched successfully",
            "count": queryset.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    # CREATE DATA
    def post(self, request):
        serializer = PendingBillGrnlistSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "message": "Data created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "message": "Validation error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    




class BillRegisterAPIView(APIView):
    
    def get(self, request, pk=None):

        # SINGLE
        if pk:
            try:
                obj = BillRegister.objects.get(id=pk)

            except BillRegister.DoesNotExist:
                return Response({
                    "message": "Data not found"
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = BillRegisterSerializer(obj)

            return Response({
                "message": "Single data fetched successfully",
                "data": serializer.data
            })

        queryset = BillRegister.objects.all().order_by('-id')
        serializer = BillRegisterSerializer(queryset, many=True)

        return Response({
            "message": "Data fetched successfully",
            "count": queryset.count(),
            "data": serializer.data
        })

    # POST
    def post(self, request):
        serializer = BillRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({
                "message": "Data created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    # PUT
    def put(self, request, pk):
        try:
            obj = BillRegister.objects.get(id=pk)

        except BillRegister.DoesNotExist:
            return Response({
                "message": "Data not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = BillRegisterSerializer(
            obj,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response({
                "message": "Data updated successfully",
                "data": serializer.data
            })

        return Response({
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    def delete(self, request, pk):
        try:
            obj = BillRegister.objects.get(id=pk)

        except BillRegister.DoesNotExist:
            return Response({
                "message": "Data not found"
            }, status=status.HTTP_404_NOT_FOUND)

        obj.delete()

        return Response({
            "message": "Data deleted successfully"
        })
    


from .utils import create_bill_no
class GenerateBillNumberAPIView(APIView):
    def get(self, request):
        try:
            bill_no = create_bill_no()

            return Response({
                "message": "Bill number generated successfully",
                "bill_no": bill_no
            }, status=status.HTTP_200_OK)

        except ValueError as e:

            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


from Store.models import InwardChallan2
from Store.serializers import InwardChallanSerializer

class InwardChallanDateFilterAPIView(APIView):
    def get(self, request):
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        supplier_name = request.GET.get('supplier_name')

        queryset = InwardChallan2.objects.all().order_by('-id')

        if supplier_name:
            queryset = queryset.filter(
                SupplierName__icontains=supplier_name
            )

        if from_date and to_date:
            try:
                from_date_obj = datetime.strptime(
                    from_date,
                    "%Y-%m-%d"
                ).date()

                to_date_obj = datetime.strptime(
                    to_date,
                    "%Y-%m-%d"
                ).date()

                # ⚠ InwardDate is CharField
                queryset = queryset.filter(
                    InwardDate__range=[
                        str(from_date_obj),
                        str(to_date_obj)
                    ]
                )

            except ValueError:

                return Response(
                    {
                        "message": "Invalid date format. Use YYYY-MM-DD"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = InwardChallanSerializer(
            queryset,
            many=True
        )

        return Response(
            {
                "message": "Data fetched successfully",
                "count": queryset.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    


class JobworkBillRegisterAPIView(APIView):
    def get(self, request, pk=None):
        try:
            if pk:
                obj = JobworkBillRegister.objects.get(id=pk)
                serializer = JobworkBillRegisterSerializer(obj)

                return Response({
                    "message": "Data fetched successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)

            queryset = JobworkBillRegister.objects.all().order_by('-id')
            serializer = JobworkBillRegisterSerializer(queryset, many=True)

            return Response({
                "message": "Data fetched successfully",
                "count": queryset.count(),
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except JobworkBillRegister.DoesNotExist:
            return Response({
                "message": "Data not found"
            }, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = JobworkBillRegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "message": "Data created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "message": "Validation error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            obj = JobworkBillRegister.objects.get(id=pk)

        except JobworkBillRegister.DoesNotExist:
            return Response({
                "message": "Data not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = JobworkBillRegisterSerializer(
            obj,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response({
                "message": "Data updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "message": "Validation error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            obj = JobworkBillRegister.objects.get(id=pk)

        except JobworkBillRegister.DoesNotExist:
            return Response({
                "message": "Data not found"
            }, status=status.HTTP_404_NOT_FOUND)

        obj.delete()

        return Response({
            "message": "Data deleted successfully"
        }, status=status.HTTP_200_OK)
    


from .utils import create_jobwork_bill_no
class GeneratejobworkBillNumberAPIView(APIView):
    def get(self, request):
        try:
            bill_no = create_jobwork_bill_no()

            return Response({
                "message": "Bill number generated successfully",
                "bill_no": bill_no
            }, status=status.HTTP_200_OK)

        except ValueError as e:

            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from weasyprint import HTML
from decimal import Decimal
from .models import BillRegister


def generate_billregister_pdf(request, pk):
    bill = get_object_or_404(BillRegister, pk=pk)
    items = bill.items.all()

    sub_total = Decimal('0.00')
    total_cgst = Decimal('0.00')
    total_sgst = Decimal('0.00')
    total_igst = Decimal('0.00')

    for item in items:
        qty = Decimal(item.grn_qty or 0)
        rate = Decimal(item.rate or 0)
        discount = Decimal(item.discount or 0)

        item.sub_total = qty * rate
        item.discount_amount = (item.sub_total * discount) / 100

        sub_total += item.sub_total
        total_cgst += Decimal(item.cgst_amt or 0)
        total_sgst += Decimal(item.sgst_amt or 0)
        total_igst += Decimal(item.igst_amt or 0)

    grand_total = (
        sub_total
        + total_cgst
        + total_sgst
        + total_igst
    )

    context = {
        "bill": bill,
        "items": items,
        "sub_total": sub_total,
        "total_cgst": total_cgst,
        "total_sgst": total_sgst,
        "total_igst": total_igst,
        "grand_total": grand_total,
    }

    template = get_template("bill_register_pdf.html")
    html_content = template.render(context)

    pdf_file = HTML(string=html_content).write_pdf()

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'inline; filename="bill_register_{bill.no}.pdf"'
    )

    return response



from rest_framework.decorators import api_view




@api_view(['GET'])
def generate_jobwork_pdf(request, id):

    grn_detail = get_object_or_404(
        InwardChallan2.objects.prefetch_related(
            'InwardChallanTable',
             'InwardChallanGSTDetails'  
        ),
        id=id
    )

    grn_items = grn_detail.InwardChallanTable.all()
    gst_items = grn_detail.InwardChallanGSTDetails.all()

    template = get_template('index.html')

    html_content = template.render({
        'grn_detail': grn_detail,
        'grn_items': grn_items,
        'gst_items': gst_items
    })

    pdf_file = HTML(
        string=html_content,
        base_url=request.build_absolute_uri('/')
    ).write_pdf()

    response = HttpResponse(
        pdf_file,
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'inline; filename="jobwork_grn_{id}.pdf"'
    )

    return response


from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from weasyprint import HTML

from .models import JobworkBillRegister

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from weasyprint import HTML

from .models import JobworkBillRegister


def generate_jobwork_bill_pdf(request, pk):

    bill = get_object_or_404(JobworkBillRegister, pk=pk)

    items = bill.items.all()

    context = {
        "bill": bill,
        "items": items,

        # Direct values from model
        "sub_total": bill.sub_total,
        "total_discount": bill.dis_total,

        "total_cgst": bill.cgst_total,
        "total_sgst": bill.sgst_total,
        "total_igst": bill.igst_total,

        "total_gst": bill.total_tax,

        "other_charges": bill.other_charge,

        "grand_total": bill.final_amount,
    }

    template = get_template(
        "jobwork_bill_register_pdf.html"
    )

    html_content = template.render(context)

    pdf_file = HTML(
        string=html_content,
        base_url=request.build_absolute_uri("/")
    ).write_pdf()

    response = HttpResponse(
        pdf_file,
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'inline; filename="jobwork_bill_{bill.bill_no}.pdf"'
    )

    return response



from Store.models import (
    GrnGenralDetail,
    NewGrnList,
    GrnGst,
    GrnGstTDC,
    RefTC
)


@api_view(['GET'])
def generate_purchase_grn_pdf(request, id):

    # MAIN GRN DETAIL
    grn_detail = get_object_or_404(
        GrnGenralDetail.objects.prefetch_related(
            'NewGrnList',
            'GrnGst',
            'GrnGstTDC',
            'RefTC'
        ),
        id=id
    )

    grn_items = grn_detail.NewGrnList.all()

    gst_items = grn_detail.GrnGst.all()

    tax_detail = grn_detail.GrnGstTDC.first()
    ref_tc_items = grn_detail.RefTC.all()
    template = get_template('PurchaseBill.html')


    html_content = template.render({
        'grn_detail': grn_detail,
        'grn_items': grn_items,
        'gst_items': gst_items,
        'tax_detail': tax_detail,
        'ref_tc_items': ref_tc_items,
    })

    pdf_file = HTML(
        string=html_content,
        base_url=request.build_absolute_uri('/')
    ).write_pdf()

    # RESPONSE
    response = HttpResponse(
        pdf_file,
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'inline; filename="Purchase_GRN_{id}.pdf"'
    )

    return response



class GeneralLedgerMasterAPIView(APIView):

    # GET ALL / GET SINGLE
    def get(self, request, pk=None):
        if pk:
            try:
                obj = GeneralLedgerMaster.objects.get(id=pk)
            except GeneralLedgerMaster.DoesNotExist:
                return Response(
                    {"message": "Data not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = GeneralLedgerMasterSerializer(obj)
            return Response(serializer.data)

        queryset = GeneralLedgerMaster.objects.all().order_by('-id')
        serializer = GeneralLedgerMasterSerializer(queryset, many=True)
        return Response(serializer.data)

    # CREATE
    def post(self, request):
        serializer = GeneralLedgerMasterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "General Ledger created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # UPDATE
    def put(self, request, pk):
        try:
            obj = GeneralLedgerMaster.objects.get(id=pk)
        except GeneralLedgerMaster.DoesNotExist:
            return Response(
                {"message": "Data not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = GeneralLedgerMasterSerializer(
            obj,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "General Ledger updated successfully",
                    "data": serializer.data
                }
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    def delete(self, request, pk):
        try:
            obj = GeneralLedgerMaster.objects.get(id=pk)
        except GeneralLedgerMaster.DoesNotExist:
            return Response(
                {"message": "Data not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        obj.delete()

        return Response(
            {"message": "General Ledger deleted successfully"},
            status=status.HTTP_200_OK
        )
    


## hsn_code wise data from sales.debitnote,invoice,jowrkdetails
from rest_framework.views import APIView
from rest_framework.response import Response
from Sales.models import *

class HSNSummaryAPIView(APIView):

    def get(self, request):

        report_type = request.GET.get("type", "Sales")

        hsn_summary = {}

        # ======================================================
        # COMMON FUNCTION
        # ======================================================

        def add_data(
            hsn,
            description="",
            qty=0,
            total_amt=0,
            taxable=0,
            cgst_amt=0,
            sgst_amt=0,
            igst_amt=0,
            cess=0,
            tcs_amt=0,
            gst_per=0,
            uom="NOS",
            group_name="FG",
            supply_type="GST Sales"
        ):

            if not hsn:
                return

            if hsn not in hsn_summary:
                hsn_summary[hsn] = {
                    "hsn_sac": hsn,
                    "description": description,
                    "type_of_supply": supply_type,
                    "group": group_name,
                    "uom": uom,
                    "total_qty": 0,
                    "total_amt": 0,
                    "gst_percent": gst_per,
                    "taxable_value": 0,
                    "igst_amt": 0,
                    "cgst_amt": 0,
                    "sgst_amt": 0,
                    "cess": 0,
                    "tcs_amt": 0,
                    "total_gst_amt": 0,
                }

            hsn_summary[hsn]["total_qty"] += float(qty or 0)
            hsn_summary[hsn]["total_amt"] += float(total_amt or 0)
            hsn_summary[hsn]["taxable_value"] += float(taxable or 0)
            hsn_summary[hsn]["igst_amt"] += float(igst_amt or 0)
            hsn_summary[hsn]["cgst_amt"] += float(cgst_amt or 0)
            hsn_summary[hsn]["sgst_amt"] += float(sgst_amt or 0)
            hsn_summary[hsn]["cess"] += float(cess or 0)
            hsn_summary[hsn]["tcs_amt"] += float(tcs_amt or 0)

            hsn_summary[hsn]["total_gst_amt"] += (
                float(igst_amt or 0)
                + float(cgst_amt or 0)
                + float(sgst_amt or 0)
            )

        # ======================================================
        # SALES INVOICE
        # ======================================================

        invoice_items = InvoiceItemdetails.objects.all().select_related("invoice")

        for item in invoice_items:

            gst = GstdetailsInvoice.objects.filter(
                invoice=item.invoice
            ).first()

            qty = item.inv_qty or 0
            rate = float(item.rate or 0)

            total_amt = qty * rate

            taxable = gst.assessble_value if gst else 0

            cgst_amt = gst.cgst_amt if gst else 0
            sgst_amt = gst.sgst_amt if gst else 0
            igst_amt = gst.igst_amt if gst else 0
            tcs_amt = gst.tcs if gst else 0

            gst_per = 0

            if gst:
                gst_per = (
                    float(gst.cgst or 0)
                    + float(gst.sgst or 0)
                    + float(gst.igst or 0)
                )

            add_data(
                hsn=item.hsn_code,
                description=item.description,
                qty=qty,
                total_amt=total_amt,
                taxable=taxable,
                cgst_amt=cgst_amt,
                sgst_amt=sgst_amt,
                igst_amt=igst_amt,
                tcs_amt=tcs_amt,
                gst_per=gst_per,
            )

        # ======================================================
        # JOBWORK GST INVOICE
        # ======================================================

        jobwork_items = GSTJobworkItemDetails.objects.all().select_related("invoice")

        for item in jobwork_items:

            gst = GSTJobworkGSTDetails.objects.filter(
                invoice=item.invoice
            ).first()

            qty = float(item.invoice_qty_nos or 0)
            rate = float(item.jobwork_rate or 0)

            total_amt = qty * rate

            taxable = gst.assessable_value if gst else 0

            cgst_amt = gst.cgst_amt if gst else 0
            sgst_amt = gst.sgst_amt if gst else 0
            igst_amt = gst.igst_amt if gst else 0
            tcs_amt = gst.tcs_amt if gst else 0

            gst_per = (
                float(gst.cgst or 0)
                + float(gst.sgst or 0)
                + float(gst.igst or 0)
            ) if gst else 0

            add_data(
                hsn=item.hsn_code,
                description=item.description,
                qty=qty,
                total_amt=total_amt,
                taxable=taxable,
                cgst_amt=cgst_amt,
                sgst_amt=sgst_amt,
                igst_amt=igst_amt,
                tcs_amt=tcs_amt,
                gst_per=gst_per,
            )

        # ======================================================
        # DEBIT NOTE
        # ======================================================

        debit_items = DebitNoteIteam.objects.all().select_related("debit_note")

        for item in debit_items:

            add_data(
                hsn=item.hsn_code,
                description=item.item_description,
                qty=item.quantity or 0,
                total_amt=item.amount or 0,
                taxable=item.subtotal or 0,
                cgst_amt=item.cgst or 0,
                sgst_amt=item.sgst or 0,
                igst_amt=item.igst or 0,
                tcs_amt=item.tcs or 0,
                gst_per=(
                    float(item.cgst or 0)
                    + float(item.sgst or 0)
                    + float(item.igst or 0)
                ),
            )

        # ======================================================
        # FINAL DATA
        # ======================================================

        final_data = list(hsn_summary.values())

        grand_total = {
            "total_qty": 0,
            "total_amt": 0,
            "taxable_value": 0,
            "igst_amt": 0,
            "cgst_amt": 0,
            "sgst_amt": 0,
            "cess": 0,
            "tcs_amt": 0,
            "total_gst_amt": 0,
        }

        for row in final_data:

            grand_total["total_qty"] += row["total_qty"]
            grand_total["total_amt"] += row["total_amt"]
            grand_total["taxable_value"] += row["taxable_value"]
            grand_total["igst_amt"] += row["igst_amt"]
            grand_total["cgst_amt"] += row["cgst_amt"]
            grand_total["sgst_amt"] += row["sgst_amt"]
            grand_total["cess"] += row["cess"]
            grand_total["tcs_amt"] += row["tcs_amt"]
            grand_total["total_gst_amt"] += row["total_gst_amt"]

        return Response({
            "status": True,
            "count": len(final_data),
            "data": final_data,
            "grand_total": grand_total
        })