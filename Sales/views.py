from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets
from .models import onwardchallan
from .models import transportdetails
from .models import vehicaldetails
from .models import outwardchallan
from .serializers import OnwardChallanSerializer
from .serializers import transportdetailsSerializer
from .serializers import vehicaldetailsSerializer
from .serializers import outwardchallanSerializer
from .utils import create_challanNumber
from All_Masters.models import Item as Item2
from Purchase.serializers import ItemSerializer, ItemDetailSerializer
from Purchase.models import PurchasePO
from django.db.models import Q


class OnwardChallanViewSet(viewsets.ModelViewSet):
    queryset = onwardchallan.objects.all()
    serializer_class = OnwardChallanSerializer
class transportdetailsview(viewsets.ModelViewSet):
    queryset=transportdetails.objects.all()
    serializer_class=transportdetailsSerializer

class vehicaldetailsview(viewsets.ModelViewSet):
    queryset=vehicaldetails.objects.all()
    serializer_class=vehicaldetailsSerializer
class outwardchallanview(viewsets.ModelViewSet):
    queryset=outwardchallan.objects.all()
    serializer_class=outwardchallanSerializer


class OnwardChallanViewSet(viewsets.ModelViewSet):
    queryset         = onwardchallan.objects.all()
    serializer_class = OnwardChallanSerializer





class deletechallan(APIView):
    def delete(self, request,id):
        # challan_no = request.data.get('challan_no')
        # if not challan_no:
        #     return Response({'error': 'challan_no is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            challan = onwardchallan.objects.get(challan_no=id)
            challan.delete()
            return Response({'message': f'Challan {id} deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except onwardchallan.DoesNotExist:
            return Response({'error': 'Challan not found'}, status=status.HTTP_404_NOT_FOUND)


class generate_unique_challan_number(APIView):
    def get(self, request):
        try:
            challan_no = create_challanNumber()
            return Response({"Challan_no" : challan_no}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class deletetransportdetails(APIView):
    def delete(self,request,name):
        try:
            transport_name=transportdetails.objects.get(transport_name=name)
            transport_name.delete()
            return Response({'message': f'transport_name {name} deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except transportdetails.DoesNotExist:
            return Response({'error': 'transport_name not found'}, status=status.HTTP_404_NOT_FOUND)


        
class edittransportdetails(APIView):
    def put(self, request, name):
        try:
            # Find the transportdetails by transport_name
            transport_obj = transportdetails.objects.get(transport_name=name)
        except transportdetails.DoesNotExist:
            return Response({'error': 'transport_name not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get new EWAY_bill_no from request body
        new_eway_bill_no = request.data.get('EWAY_bill_no')
        if not new_eway_bill_no:
            return Response({'error': 'EWAY_bill_no is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update
        transport_obj.EWAY_bill_no = new_eway_bill_no
        transport_obj.save()

        return Response({
            'message': f'transport_name {name} updated successfully',
            'transport_name': transport_obj.transport_name,
            'EWAY_bill_no': transport_obj.EWAY_bill_no,
            'serial_no': transport_obj.serial_no,
        }, status=status.HTTP_200_OK)

class editvehicaldetails(APIView):
    def put(self, request, vehical_no):
        try:
            vehicle = vehicaldetails.objects.get(vehical_no=vehical_no)
        except vehicaldetails.DoesNotExist:
            return Response({'error': 'Vehicle not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = vehicaldetailsSerializer(vehicle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class deletevehicaldetails(APIView):
    def delete(self,request,name):
        try:
            vehical_no=vehicaldetails.objects.get(vehical_no=name)
            vehical_no.delete()
            return Response({'message':f'vehical_no {name} deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except transportdetails.DoesNotExist:
            return Response({'error':'vehical_no not found'}, status=status.HTTP_404_NOT_FOUND)


class purchaseview(APIView):
    def post(self, request):
        
        purchase_order = request.data.get('purchase_order')
        item_code = request.data.get('item_code')
        description = request.data.get('description')
        quantity = request.data.get('quantity')
        unit_price = request.data.get('unit_price')
        total_price = request.data.get('total_price')

    
        if not purchase_order or not item_code:
            return Response(
                {"error": "purchase_order and item_code are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = Item2.objects.all()
        queryset = queryset.filter(purchase_order=purchase_order, item_code=item_code)

        if description:
            queryset = queryset.filter(description__icontains=description)
        if quantity:
            queryset = queryset.filter(quantity=quantity)
        if unit_price:
            queryset = queryset.filter(unit_price=unit_price)
        if total_price:
            queryset = queryset.filter(total_price=total_price)

        serializer = ItemSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class challanview(APIView):
    def get(self, request):
        challan_no = request.query_params.get('challan_no')
        if not challan_no:
            return Response({"error": "challan_no parameter is required."}, status=400)

        try:
            challan = onwardchallan.objects.get(challan_no=challan_no)
        except onwardchallan.DoesNotExist:
            return Response({"error": "Challan not found."}, status=404)

        serializer = OnwardChallanSerializer(challan)
        return Response(serializer.data)
    
from Purchase.models import NewJobWorkItemDetails
from Purchase.serializers import NewJobWorkItemDetailsSerializer

# class inwardchallanview(APIView):
#     def get(self, request):
#         supplier = request.query_params.get('supplier')
#         if not supplier:
#             return Response({"error": "supplier parameter is required."}, status=400)

#         supplier = supplier.strip()
#         purchase_orders = PurchasePO.objects.filter(
#             Q(Supplier__icontains=supplier) |
#             Q(Supplier__iexact=supplier)
#         )
#         if not purchase_orders.exists():
#             return Response(
#                 {"error": f"No PurchasePO found for supplier '{supplier}'"},
#                 status=404
#             )

#         results = []
#         all_details = []

#         for po in purchase_orders:
#             # 1) Items on this PO
#             items_qs = po.items.all()
#             items_data = ItemSerializer(items_qs, many=True).data

#             # 2) Details on this PO
#             detail_qs = po.Item_Detail_Enter.all()  # or use the related_name you set
#             details_data = NewJobWorkItemDetailsSerializer(detail_qs, many=True).data

#             # collect into the per‑PO results
#             results.append({
#                 "purchase_order_no": po.PoNo,
#                 "items": items_data,
#                 "item_details": details_data,      # <-- this is already an array
#             })

#             # also flatten into a single array if you need that
#             all_details.extend(details_data)
#             all_details.extend(items_data)

#         return Response({
#             "supplier": supplier,
#             "results": results,                  # list of per‑PO dicts
#             "all_item_details": all_details,     # flat list of every detail
#         }, status=status.HTTP_200_OK)
    

class supplierview(APIView):
    def get(self, request):
        supplier = request.query_params.get('supplier')
        if not supplier:
            return Response({"error": "supplier parameter is required."}, status=400)

        # Filter onwardchallan by vendor name
        challans = onwardchallan.objects.filter(vender__iexact=supplier)

        if not challans.exists():
            return Response({"error": f"No challans found for supplier '{supplier}'"}, status=404)

        serializer = OnwardChallanSerializer(challans, many=True)
        return Response({
            "supplier": supplier,
            "challans": serializer.data
        }, status=status.HTTP_200_OK)


from django.template.loader import get_template
from django.shortcuts import render,get_object_or_404,HttpResponse
from weasyprint import HTML
def generate_onwardchallan_pdf(request, pk):
    challan = get_object_or_404(onwardchallan, pk=pk)
    items = challan.items.all()

    total=0
    for item in items:
        item.value = (item.qtyNo or 1) * (item.wRate or 1)
        total=total+item.value
    challan.Amount=total

    context = {
        'challan': challan,
        'items': items,
    }

    template = get_template('Sales/onwardchallan_details.html')
    html_content = template.render(context)
    pdf_file = HTML(string=html_content).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="onwardchallan_{pk}.pdf"'
    return response



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from Purchase.models import *

class inwardchallanview(APIView):
    def get(self, request):
        supplier = request.query_params.get('supplier')
        if not supplier:
            return Response({"error": "supplier parameter is required."}, status=400)

        supplier = supplier.strip()
        purchase_orders = NewJobWorkPoInfo.objects.filter(
            Q(Supplier__icontains=supplier) |
            Q(Supplier__iexact=supplier)
        )
        if not purchase_orders.exists():
            return Response(
                {"error": f"No NewJobWorkPoInfo found for supplier '{supplier}'"},
                status=404
            )

        results = []
        all_details = []

        for po in purchase_orders:
            
            item_details_qs = po.Item_Detail_Enter.all()
            gst_details_qs = po.Gst_Details.all()
            schedule_line_qs = po.Schedule_Line.all()
            ship_to_add_qs = po.Ship_To_Add.all()

            items_data = NewJobWorkItemDetailsSerializer(item_details_qs, many=True).data
            # gst_data = NewJobWorkGstDetailsSerializer(gst_details_qs, many=True).data
            # schedule_data = NewJobWorkScheduleLineSerializer(schedule_line_qs, many=True).data
            # ship_to_data = NewJobWorkShipToAddSerializer(ship_to_add_qs, many=True).data

            results.append({
                "po_no": po.PoNo,
                "po_type": po.PoType,
                "supplier": po.Supplier,
                "po_date": po.PoDate,
                "items": items_data,
                # "gst_details": gst_data,
                # "schedule_lines": schedule_data,
                # "ship_to_address": ship_to_data,
            })

            # Flatten all details if needed
            all_details.extend(items_data)
            # all_details.extend(gst_data)
            # all_details.extend(schedule_data)
            # all_details.extend(ship_to_data)

        return Response({
            "supplier": supplier,
            "results": results,
            "all_details": all_details,
        }, status=status.HTTP_200_OK)




# class inwardchallanview(APIView):
#     def get(self, request):
#         supplier = request.query_params.get('supplier')

#         if not supplier:
#             return Response({"error": "supplier parameter is required."}, status=400)

#         supplier = supplier.strip()
#         purchase_orders = NewJobWorkPoInfo.objects.filter(
#             Q(Supplier__icontains=supplier) |
#             Q(Supplier__iexact=supplier)
#         )

#         if not purchase_orders.exists():
#             return Response(
#                 {"error": f"No NewJobWorkPoInfo found for supplier '{supplier}'"},
#                 status=404
#             )

#         results = []
#         all_details = []

#         for po in purchase_orders:
           
#             item_details_qs = po.Item_Detail_Enter.filter(item_type__iexact="FG")

#             items_data = NewJobWorkItemDetailsSerializer(item_details_qs, many=True).data

#             # Skip PO if no FG items
#             if not items_data:
#                 continue

#             results.append({
#                 "po_no": po.PoNo,
#                 "po_type": po.PoType,
#                 "supplier": po.Supplier,
#                 "po_date": po.PoDate,
#                 "items": items_data,
#             })

#             all_details.extend(items_data)

#         return Response({
#             "supplier": supplier,
#             "item_type": "FG",   # Always FG
#             "results": results,
#             "all_details": all_details,
#         }, status=status.HTTP_200_OK)



class InwardChallanRMView(APIView):
    def get(self, request):
        supplier = request.query_params.get('supplier')

        if not supplier:
            return Response({"error": "supplier parameter is required."}, status=400)

        supplier = supplier.strip()
        purchase_orders = NewJobWorkPoInfo.objects.filter(
            Q(Supplier__icontains=supplier) |
            Q(Supplier__iexact=supplier)
        )

        if not purchase_orders.exists():
            return Response(
                {"error": f"No NewJobWorkPoInfo found for supplier '{supplier}'"},
                status=404
            )

        results = []
        # all_details = []

        for po in purchase_orders:
            #  Always filter items with item_type = 'RM'
            item_details_qs = po.Item_Detail_Enter.filter(item_type__iexact="RM")

            items_data = NewJobWorkItemDetailsSerializer(item_details_qs, many=True).data

            # Skip PO if no RM items
            if not items_data:
                continue

            results.append({
                "po_no": po.PoNo,
                "po_type": po.PoType,
                "supplier": po.Supplier,
                "po_date": po.PoDate,
                "items": items_data,
            })

            # all_details.extend(items_data)

        return Response({
            "supplier": supplier,
            "item_type": "RM",   # Always RM
            "results": results,
            # "all_details": all_details,
        }, status=status.HTTP_200_OK)

from .utils import create_reworknumber
class generate_unique_rework_number(APIView):
    def get(self, request):
        try:
            rework_no = create_reworknumber()
            return Response({"Rework_no": rework_no}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, F, Value, FloatField
from django.db.models.functions import Cast, Coalesce
from collections import defaultdict

from Store.models import MaterialChallan, MaterialChallanTable
from Production.models import   ProductionEntry


def safe_float(value):
    try:
        return float(value)
    except:
        return 0


class ItemFullReport(APIView):
    """
    ONE API = HeatNo Summary + Production Summary
    """

    def get(self, request):
        item = request.query_params.get("item")
        operation = request.query_params.get("operation")
        prod_no = request.query_params.get("prod_no")

        if not item:
            return Response(
                {"error": "item parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # =====================================================
        #         🔹 1) Heat No Wise Qty Summary
        # =====================================================
        challans = MaterialChallan.objects.filter(Item__icontains=item)

        if not challans.exists():
            heat_qty_list = []
        else:
            heat_qty_data = (
                MaterialChallanTable.objects
                .filter(MaterialChallanDetail__in=challans)
                .values("HeatNo")
                .annotate(
                    total_qty=Sum(
                        Coalesce(Cast(F("Qty"), FloatField()), Value(0.0))
                    )
                )
                .order_by("HeatNo")
            )

            heat_qty_list = [
                {
                    "HeatNo": entry["HeatNo"] if entry["HeatNo"] else "No HeatNo",
                    "Qty": entry["total_qty"]
                }
                for entry in heat_qty_data
            ]

        # =====================================================
        #         🔹 2) Production Operation-wise Lot Summary
        # =====================================================
        entries = ProductionEntry.objects.filter(item=item)

        if operation:
            entries = entries.filter(operation=operation)

        if prod_no:
            entries = entries.filter(Prod_no=prod_no)

        prod_result = {}

        for e in entries:
            opno = e.operation
            lot = (e.lot_no or "").split("|")[0]
            qty = safe_float(e.prod_qty or 0)

            if opno not in prod_result:
                prod_result[opno] = defaultdict(float)

            prod_result[opno][lot] += qty

        prod_output = {
            op: [{"lot_no": lot, "prod_qty": qty} for lot, qty in lots.items()]
            for op, lots in prod_result.items()
        }

        # =====================================================
        #              🔹 FINAL COMBINED RESPONSE
        # =====================================================

        return Response({
            "item": item,
            "heat_qty_summary": heat_qty_list,
            "production_summary": prod_output
        }, status=status.HTTP_200_OK)



from .serializers import *
from .models import *
class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            print("❌ VALIDATION ERRORS →", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NewsalesOrederViewSet(viewsets.ModelViewSet):
    queryset = NewSalesOrder.objects.all()
    serializer_class= NewSalesOrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("❌ SERIALIZER ERRORS:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



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
    


from All_Masters.models import ItemTable,TaxDetails
from All_Masters.serializers import ItemTableSerializer2

class ItemTableListView(APIView):
    def get(self, request):
        items = ItemTable.objects.all().order_by('id')
        serializer = ItemTableSerializer2(items, many=True)

        data = serializer.data  # serialized itemtable data

        # attach tax details manually
        for item in data:
            hsn_code = item.get("HSN_SAC_Code")

            if hsn_code:
                tax = TaxDetails.objects.filter(
                    HSN_SAC_Code=hsn_code
                ).values().first()
                item["tax_details"] = tax
            else:
                item["tax_details"] = None

        return Response({
            "message": "Items fetched successfully",
            "count": len(data),
            "data": data
        })


from .utils import create_invoiceno
class generate_invoice_number(APIView):
    def get(self ,request):
        try:
            invoice_no=create_invoiceno()
            return Response ({"Invoice_no": invoice_no}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# class LastOperationProdQtyAPI(APIView):

#     def get(self, request):
#         query = request.query_params.get('q', '').strip()
#         if not query:
#             return Response(
#                 {"error": 'Search query "q" is required'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         item = ItemTable.objects.filter(
#             Q(Part_Code__icontains=query) |
#             Q(part_no__icontains=query) |
#             Q(Name_Description__icontains=query)
#         ).first()

#         if not item:
#             return Response(
#                 {"error": "Item not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         bom_items = BOMItem.objects.filter(item=item)

#         if not bom_items.exists():
#             return Response(
#                 {"error": "No BOM found for item"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         last_op_data = None
#         last_op_no = -1

#         for bom in bom_items:
#             if not bom.OPNo:
#                 continue

#             try:
#                 op_no_int = int(bom.OPNo.strip())
#             except ValueError:
#                 continue

#             production = ProductionEntry.objects.filter(
#                 item__icontains=item.Part_Code,
#                 operation__startswith=bom.OPNo
#             ).order_by('-id').first()   # 🔥 latest entry for that OP

#             prod_qty = float(production.prod_qty) if production else 0.0

#             # 🔥 Pick highest OPNo
#             if op_no_int > last_op_no:
#                 last_op_no = op_no_int
#                 last_op_data = {
#                     "part_code": item.Part_Code,
#                     "part_no": item.part_no,
#                     "Name_Description": item.Name_Description,
#                     "OPNo": bom.OPNo,
#                     "Operation": bom.Operation,
#                     "prod_qty": prod_qty
#                 }

#         if not last_op_data:
#             return Response(
#                 {"error": "No production data found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         return Response(
#             {"last_operation": last_op_data},
#             status=status.HTTP_200_OK
#         )


from All_Masters.models import BOMItem

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


class DebitNoteViewSet(viewsets.ModelViewSet):
    queryset = DebitNote.objects.prefetch_related("items").all()
    serializer_class = DebitNoteSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Debit Note deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

from .utils import create_debitNote
class GenerateDebitNoteNumber(APIView):
    def get(self, request):
        try:
            debit_note_no = create_debitNote()
            return Response(
                {"debit_note_no": debit_note_no},
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        



from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from num2words import num2words

from Purchase.models import PurchasePO
from All_Masters.models import Item as Item2


# class PurchasePOBySupplierAPIView(APIView):
#     def get(self, request):
#         supplier_name = request.query_params.get("supplier")

#         if not supplier_name:
#             return Response(
#                 {"error": "supplier query parameter is required"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         pos = PurchasePO.objects.prefetch_related(
#             "Item_Detail_Enter",
#             "Gst_Details",
#             "Item_Details_Other",
           
#         ).filter(Supplier__iexact=supplier_name)

#         result = []

#         for po in pos:

#             # 🔹 Supplier Master (same as PDF)
#             supplier_item = Item2.objects.filter(number=po.CodeNo).first()

#             # 🔹 Item Details
#             item_details = []
#             for i in po.Item_Detail_Enter.all():
#                 item_details.append({
#                     "item": i.Item,
#                     "description": i.ItemDescription,
#                     "size": i.ItemSize,
#                     "rate": i.Rate,
#                     "discount": i.Disc,
#                     "qty": i.Qty,
#                     "unit": i.Unit,
#                     "particular": i.Particular,
#                     "mill_name": i.Mill_Name,
                    
#                 })

#             # 🔹 GST Details
#             gst_details = []
#             total_gst_sum = 0

#             for gst in po.Gst_Details.all(): 
#                 gst_details.append({
#                     "item_code": gst.ItemCode,
#                     "hsn": gst.HSN,
#                     "rate": gst.Rate,
#                     "qty": gst.Qty,
#                     "sub_total": gst.SubTotal,
#                     "discount": gst.Discount,
#                     "packing": gst.Packing,
#                     "transport": gst.Transport,
#                     "assessable_value": gst.AssValue,
#                     "cgst": gst.CGST,
#                     "sgst": gst.SGST,
#                     "igst": gst.IGST,
#                     "vat": gst.Vat,
#                     "cess": gst.Cess,
#                     "total": gst.Total,
#                 })
            

#                 if gst.Total:
#                     total_gst_sum += gst.Total

#             # 🔹 Amount in words (same as PDF)
#             amount_words = f"Rs. {num2words(int(total_gst_sum), lang='en_IN').title()} Only"

#             result.append({
#                 "po_basic_details": {
#                     "PoNo": po.PoNo,
#                     "PoDate": po.PoDate,
#                     "Field": po.field,
#                     "Supplier": po.Supplier,
#                     "Plant": po.Plant,
#                     "Series": po.Series,
#                     "PaymentTerms": po.PaymentTerms,
#                     "DeliveryDate": po.DeliveryDate,
#                     "ApprovedStatus": po.Approved_Status,
#                 },
                
#                 "item_details": item_details,
#                 "gst_details": gst_details,
                            
               
#                 "total_gst_sum": total_gst_sum,
#                 "total_in_words": amount_words,
#             })

#         return Response(result, status=status.HTTP_200_OK)



from datetime import datetime
from Purchase.models import PurchasePO
from All_Masters.models import Item as Item2


class PurchasePOBySupplierAPIView(APIView):
    def get(self, request):
        supplier_name = request.query_params.get("supplier")
        from_date = request.query_params.get("from_date")
        to_date = request.query_params.get("to_date")

        if not supplier_name:
            return Response(
                {"error": "supplier query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        pos = PurchasePO.objects.prefetch_related(
            "Item_Detail_Enter",
            "Gst_Details",
            "Item_Details_Other",
        ).filter(Supplier__iexact=supplier_name)

        # 🔹 Date range filter
        if from_date and to_date:
            try:
                from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
                to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
                pos = pos.filter(PoDate__range=[from_date, to_date])
            except ValueError:
                return Response(
                    {"error": "Invalid date format. Use YYYY-MM-DD"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        result = []

        for po in pos:

            # 🔹 Item Details
            item_details = []
            for i in po.Item_Detail_Enter.all():
                item_details.append({
                    "item": i.Item,
                    "description": i.ItemDescription,
                    "size": i.ItemSize,
                    "rate": i.Rate,
                    "discount": i.Disc,
                    "qty": i.Qty,
                    "unit": i.Unit,
                    "particular": i.Particular,
                    "mill_name": i.Mill_Name,
                })

            # 🔹 GST Details
            gst_details = []
            total_gst_sum = 0

            for gst in po.Gst_Details.all():
                gst_details.append({
                    "item_code": gst.ItemCode,
                    "hsn": gst.HSN,
                    "rate": gst.Rate,
                    "qty": gst.Qty,
                    "sub_total": gst.SubTotal,
                    "discount": gst.Discount,
                    "packing": gst.Packing,
                    "transport": gst.Transport,
                    "assessable_value": gst.AssValue,
                    "cgst": gst.CGST,
                    "sgst": gst.SGST,
                    "igst": gst.IGST,
                    "vat": gst.Vat,
                    "cess": gst.Cess,
                    "total": gst.Total,
                })

                if gst.Total:
                    total_gst_sum += gst.Total

            amount_words = f"Rs. {num2words(int(total_gst_sum), lang='en_IN').title()} Only"

            result.append({
                "po_basic_details": {
                    "PoNo": po.PoNo,
                    "PoDate": po.PoDate,
                    "Field": po.field,
                    "Supplier": po.Supplier,
                    "Plant": po.Plant,
                    "Series": po.Series,
                    "PaymentTerms": po.PaymentTerms,
                    "DeliveryDate": po.DeliveryDate,
                    "ApprovedStatus": po.Approved_Status,
                },
                "item_details": item_details,
                "gst_details": gst_details,
                "total_gst_sum": total_gst_sum,
                "total_in_words": amount_words,
            })

        return Response(result, status=status.HTTP_200_OK)




# class NewgstsalesreturnViewSet(viewsets.ModelViewSet):
#     queryset = Newgstsalesreturn.objects.prefetch_related("items").all()
#     serializer_class = NewgstsalesreturnSerializer
    

class NewgstsalesreturnViewSet(viewsets.ModelViewSet):
    queryset = Newgstsalesreturn.objects.prefetch_related("items").all()
    serializer_class = NewgstsalesreturnSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            print("ERROR:", serializer.errors)   #  ye important hai
            return Response(serializer.errors, status=400)

        self.perform_create(serializer)
        return Response(serializer.data, status=201)

from .utils import create_sales_return_no
class GenerateSalesReturnNumber(APIView):
    def get(self, request):
        try:
            sales_return_no = create_sales_return_no()
            return Response(
                {"sales_return_no": sales_return_no},
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
from django.template.loader import render_to_string
# class DebitNotePDFAPIView(APIView):

#     def get(self, request, pk):
#         debit = DebitNote.objects.get(id=pk)
#         items = DebitNoteIteam.objects.filter(debit_note=debit)

#         grand_total = sum(
#             item.grand_total or 0 for item in items
#         )
#         copies = [
#             "ORIGINAL FOR RECIPIENT",
#             "DUPLICATE FOR TRANSPORTER",
#             "TRIPLICATE FOR SUPPLIER"
#         ]

#         html_string = render_to_string(
#             'Sales/debit_note_pdf.html',
#             {
#                 'debit': debit,
#                 'items': items,
#                 'grand_total': grand_total,
#                 'copies': copies
#             }
#         )

#         html = HTML(string=html_string)
#         pdf = html.write_pdf()

#         response = HttpResponse(pdf, content_type='application/pdf')
#         response['Content-Disposition'] = (
#             f'inline; filename="DebitNote_{debit.debit_note_no}.pdf"'
#         )

#         return response


from num2words import num2words

def amount_to_words(amount):
    amount = amount or 0
    rupees = int(amount)
    paise = round((amount - rupees) * 100)

    words = f"Rupees {num2words(rupees, lang='en_IN').title()}"
    if paise > 0:
        words += f" And {num2words(paise).title()} Paise"
    words += " Only"
    return words


from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework.views import APIView
from weasyprint import HTML

class DebitNotePDFAPIView(APIView):

    def get(self, request, pk):
        debit = DebitNote.objects.get(id=pk)
        items = DebitNoteIteam.objects.filter(debit_note=debit)

        # 🔹 Totals
        sub_total = sum(item.subtotal or 0 for item in items)
        cgst_total = sum(item.cgst or 0 for item in items)
        sgst_total = sum(item.sgst or 0 for item in items)
        igst_total = sum(item.igst or 0 for item in items)
        grand_total = sum(item.grand_total or 0 for item in items)

        # 🔹 Amount in words
        cgst_words = amount_to_words(cgst_total)
        sgst_words = amount_to_words(sgst_total)
        igst_words = amount_to_words(igst_total)
        total_amount_words = amount_to_words(grand_total)

        # 🔹 FIXED item table height
        MAX_ROWS = 10
        item_count = items.count()
        empty_rows = range(max(0, MAX_ROWS - item_count))

        # 🔹 Copies
        copies = [
            "ORIGINAL FOR RECIPIENT",
            "DUPLICATE FOR TRANSPORTER",
            "TRIPLICATE FOR SUPPLIER"
        ]

        html_string = render_to_string(
            'Sales/debit_note_pdf.html',
            {
                'debit': debit,
                'items': items,
                'sub_total': sub_total,
                'cgst_total': cgst_total,
                'sgst_total': sgst_total,
                'igst_total': igst_total,
                'grand_total': grand_total,

                'cgst_words': cgst_words,
                'sgst_words': sgst_words,
                'igst_words': igst_words,
                'total_amount_words': total_amount_words,

                'empty_rows': empty_rows,
                'copies': copies,
            }
        )

        pdf = HTML(string=html_string).write_pdf()

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = (
            f'inline; filename="DebitNote_{debit.debit_note_no}.pdf"'
        )
        return response



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import NewSalesOrder
from .serializers import NewSalesOrderSerializer


class NewSalesOrderListAPIView(APIView):

    def get(self, request):
        customer = request.GET.get("customer")

        queryset = NewSalesOrder.objects.all().order_by("-id")

        if customer:
            queryset = queryset.filter(
                Q(customer__icontains=customer)
            )

        serializer = NewSalesOrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# from Store.models import GeneralDetails
# from Store.serializers import GeneralDetailsSerializer
# class SalesReturnListAPIView(APIView):
#     def get(self, request):
#         queryset = GeneralDetails.objects.filter(Type="Sales Return")
#         serializer = GeneralDetailsSerializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


from Store.models import GeneralDetails
from Store.serializers import GeneralDetailsSerializer
from .models import Newgstsalesreturn

class SalesReturnListAPIView(APIView):

    def get(self, request):

        # GST Sales Return me already used Gate Entry Numbers
        used_gate_entries = Newgstsalesreturn.objects.filter(
            gate_entry_no__isnull=False
        ).exclude(
            gate_entry_no=""
        ).values_list(
            "gate_entry_no",
            flat=True
        )

        # Sirf Sales Return wale GeneralDetails
        # jinka Gate Entry GST Sales Return me nahi hai
        queryset = GeneralDetails.objects.filter(
            Type="Sales Return"
        ).exclude(
            GE_No__in=used_gate_entries
        )

        serializer = GeneralDetailsSerializer(
            queryset,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )



from .utils import create_so_no
class GenerateSalesOrderNumber(APIView):
    def get(self, request):
        try:
            so_no = create_so_no()
            return Response(
                {"so_no": so_no},
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



from collections import defaultdict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class FinishOpHeatWiseProd(APIView):

    def get(self, request):
        part_no = request.query_params.get("part_no")

        if not part_no:
            return Response(
                {"error": "part_code is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        
        bom_qs = BOMItem.objects.filter(
            item__Part_Code__icontains=part_no
        )

        if not bom_qs.exists():
            return Response(
                {"error": "No BOM found for this part"},
                status=status.HTTP_404_NOT_FOUND
            )

        
        finish_bom = bom_qs.filter(Operation__icontains="FINISH")

        if finish_bom.exists():
            final_bom = finish_bom.first()
        else:
            
            final_bom = max(
                bom_qs,
                key=lambda x: int(x.OPNo) if str(x.OPNo).isdigit() else 0
            )

        final_opno = final_bom.OPNo.strip()   

       
        prod_qs = ProductionEntry.objects.filter(
            item__icontains=part_no,
            operation__startswith=final_opno
        )

        if not prod_qs.exists():
            return Response(
                {
                    "part_code": part_no,
                    "OPNo": final_opno,
                    "data": []
                },
                status=status.HTTP_200_OK
            )

       
        heat_wise = defaultdict(float)

        for prod in prod_qs:
            heat_no = getattr(prod, "heat_no", "UNKNOWN")
            heat_wise[heat_no] += float(prod.prod_qty or 0)

       
        response_data = [
            {
                "heat_no": heat_no,
                "prod_qty": round(qty, 2)
            }
            for heat_no, qty in heat_wise.items()
        ]

        return Response({
            "part_no": part_no,
            "OPNo": final_opno,
            "Operation": final_bom.Operation,
            "data": response_data
        }, status=status.HTTP_200_OK)




from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.http import HttpResponse
from weasyprint import HTML

from .models import Newgstsalesreturn 

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML

# ── num2words helper ──────────────────────────────────────────────────────────
def amount_to_words(amount):
    """Convert a numeric amount to Indian-style words (Rupees … Paise Only)."""
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return "Zero"

    rupees = int(amount)
    paise  = round((amount - rupees) * 100)

    ones = [
        '', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight',
        'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen',
        'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen',
    ]
    tens = [
        '', '', 'Twenty', 'Thirty', 'Forty', 'Fifty',
        'Sixty', 'Seventy', 'Eighty', 'Ninety',
    ]

    def _two(n):
        if n < 20:
            return ones[n]
        return (tens[n // 10] + (' ' + ones[n % 10] if n % 10 else '')).strip()

    def _to_words(n):
        if n == 0:
            return ''
        parts = []
        if n >= 10_000_000:
            parts.append(_to_words(n // 10_000_000) + ' Crore')
            n %= 10_000_000
        if n >= 100_000:
            parts.append(_to_words(n // 100_000) + ' Lakh')
            n %= 100_000
        if n >= 1_000:
            parts.append(_to_words(n // 1_000) + ' Thousand')
            n %= 1_000
        if n >= 100:
            parts.append(ones[n // 100] + ' Hundred')
            n %= 100
        if n > 0:
            parts.append(_two(n))
        return ' '.join(parts)

    rupee_words = _to_words(rupees) or 'Zero'
    result = f"Rs. {rupee_words}"
    if paise:
        result += f" and {_two(paise)} Paise"
    result += " Only"
    return result


# ── view ──────────────────────────────────────────────────────────────────────
def generate_salesreturn_pdf(request, pk):
    sales_return = get_object_or_404(Newgstsalesreturn, pk=pk)
    items = sales_return.items.all()

    subtotal     = 0.0
    total_cgst_percent = 0.0
    total_sgst_percent = 0.0
    total_igst_percent = 0.0
    total_cgst   = 0.0
    total_sgst   = 0.0
    total_igst   = 0.0
    grand_total  = 0.0

    for item in items:
        subtotal    += float(item.subtotal    or 0)
        total_cgst_percent += float(item.cgst or 0)
        total_sgst_percent += float(item.sgst or 0)
        total_igst_percent += float(item.igst or 0)
        total_cgst  += float(item.cgst_amt   or 0)
        total_sgst  += float(item.sgst_amt   or 0)
        total_igst  += float(item.igst_amt   or 0)
        grand_total += float(item.grand_total or 0)

    # Pad item list so the table always shows at least 10 rows
    min_rows   = 10
    item_count = items.count()
    empty_rows = range(max(0, min_rows - item_count))

    context = {
        "sales_return": sales_return,
        "items": items,
        "empty_rows": empty_rows,

        # Totals
        "subtotal":    subtotal,
         "cgst_percent": total_cgst_percent,
         "sgst_percent": total_sgst_percent,
         "igst_percent": total_igst_percent,
        "cgst":        total_cgst,
        "sgst":        total_sgst,
        "igst":        total_igst,
        "grand_total": grand_total,

        # Amount in words
        "cgst_words":  amount_to_words(total_cgst),
        "sgst_words":  amount_to_words(total_sgst),
        "total_words": amount_to_words(grand_total),

        # Company / party details – populate from your Party/Settings model
        # Replace the values below with actual lookups as needed.
        "company_gstin": "27AAMFS1149Q1ZH",
        "company_pan":   "AAMFS1149Q",
        "party_gstin":   getattr(sales_return, 'party_gstin', ''),
        "party_address": getattr(sales_return, 'party_address', ''),
        "party_state_code": getattr(sales_return, 'party_state_code', '27'),
        "party_pan":     getattr(sales_return, 'party_pan', 'NA'),
    }

    template     = get_template("Sales/salesreturn.html")
    html_content = template.render(context)

    pdf_file = HTML(
        string=html_content,
        base_url=request.build_absolute_uri()
    ).write_pdf()

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="sales_return_{pk}.pdf"'
    return response




# def generate_salesreturn_pdf(request, pk):
#     sales_return = get_object_or_404(Newgstsalesreturn, pk=pk)
#     items = sales_return.items.all()

#     subtotal = 0
#     total_cgst = 0
#     total_sgst = 0
#     grand_total = 0

#     for item in items:

#         item.basic_total = float(item.return_qty or 0) * float(item.rate or 0)

#         subtotal += float(item.subtotal or 0)
#         total_cgst += float(item.cgst_amt or 0)
#         total_sgst += float(item.sgst_amt or 0)
#         grand_total += float(item.grand_total or 0)


#     context = {
#         "sales_return": sales_return,
#         "items": items,
#         "subtotal": subtotal,
#         "cgst": total_cgst,
#         "sgst": total_sgst,
#         "grand_total": grand_total,

#     }
#     template = get_template("Sales/salesreturn.html")
#     html_content = template.render(context)
#     pdf_file = HTML(string=html_content, base_url=request.build_absolute_uri()).write_pdf()


#     response = HttpResponse(pdf_file, content_type="application/pdf")

#     response["Content-Disposition"] = f'inline; filename="sales_return_{pk}.pdf"'


#     return response



class GetNewgstsalesreturn(APIView):
    def get(self, request):
        queryset = Newgstsalesreturn.objects.prefetch_related("items").all()

        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        cust_name = request.query_params.get('cust_name')

        # Date Filter (Flexible)
        if start_date:
            queryset = queryset.filter(sales_return_date__gte=start_date)

        if end_date:
            queryset = queryset.filter(sales_return_date__lte=end_date)

        # Customer Filter
        if cust_name:
            queryset = queryset.filter(cust_name__icontains=cust_name)

        serializer = NewgstsalesreturnSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML
from .models import Invoice

# def generate_invoice_pdf(request, pk):
#     invoice = get_object_or_404(Invoice, pk=pk)
#     items = invoice.items.all()
#     gst = invoice.GSTdetails.first()

#     total = 0

#     # ✅ Calculate item amount
#     for item in items:
#         qty = item.inv_qty or 0
#         rate = float(item.rate or 0)
#         item.amount = qty * rate
#         total += item.amount

#     # ✅ GST Calculation (optional safe)
#     cgst = gst.cgst_amt if gst else 0
#     sgst = gst.sgst_amt if gst else 0
#     igst = gst.igst_amt if gst else 0
#     grand_total = gst.grand_total if gst else total

#     context = {
#         'invoice': invoice,
#         'items': items,
#         'total': total,
#         'gst': gst,
#         'cgst': cgst,
#         'sgst': sgst,
#         'igst': igst,
#         'grand_total': grand_total
#     }

#     template = get_template('Sales/invoice_template.html')  # 👈 create this file
#     html_content = template.render(context)

#     pdf_file = HTML(string=html_content).write_pdf()

#     response = HttpResponse(pdf_file, content_type='application/pdf')
#     response['Content-Disposition'] = f'inline; filename="invoice_{pk}.pdf"'

#     return response


def safe_float(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0
def generate_invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    items = invoice.items.all()
    gst = invoice.GSTdetails.first()

    first_item = items.first()
    
    total = 0

    for item in items:
        qty = safe_float(item.inv_qty or item.po_qty)
        rate = safe_float(item.rate)
        item.amount = qty * rate
        total += item.amount

    # ✅ FIX HERE
    taxable = safe_float(gst.assessble_value) if gst else 0
    cgst = safe_float(gst.cgst_amt) if gst else 0
    sgst = safe_float(gst.sgst_amt) if gst else 0
    igst = safe_float(gst.igst_amt) if gst else 0

    grand_total = taxable + cgst + sgst + igst

    context = {
        'invoice': invoice,
        'items': items,
        'first_item': first_item,
        'total': total,
        'gst': gst,
        'grand_total': grand_total
    }

    template = get_template('Sales/invoice_template.html')
    html = template.render(context)

    pdf = HTML(string=html).write_pdf()

    return HttpResponse(pdf, content_type='application/pdf')




class SalesRateDiffAPI(APIView):
    def get(self, request, pk=None):
        if pk:
            obj = SalesRateDiff.objects.get(pk=pk)
            serializer = SalesRateDiffSerializer(obj)
            return Response(serializer.data)

        queryset = SalesRateDiff.objects.all().order_by('-id')
        serializer = SalesRateDiffSerializer(queryset, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = SalesRateDiffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk):
        obj = SalesRateDiff.objects.get(pk=pk)
        serializer = SalesRateDiffSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        obj = SalesRateDiff.objects.get(pk=pk)
        obj.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    



from .utils import create_debit_note_no
class GenrateDebitNoteNoforsalesDiff(APIView):
    def get(self,request):
        try:
            debit_note_no =create_debit_note_no()
            return Response({"debit_note_no":debit_note_no},status=status.HTTP_200_OK) 
        except ValueError as e:
            return Response(
                {"error": str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

class InvoiceFilterAPI(APIView):
    def get(self, request):
        from_date = request.query_params.get("from_date")
        to_date = request.query_params.get("to_date")
        customer = request.query_params.get("customer")

        data = Invoice.objects.prefetch_related('items', 'GSTdetails')

        # Date filter
        if from_date and to_date:
            data = data.filter(invoice_Date__range=[from_date, to_date])

        # Customer filter
        if customer:
            data = data.filter(items__customer__icontains=customer)

        data = data.distinct()

        serializer = InvoiceSerializer(data, many=True)
        return Response(serializer.data)
    




class GSTJobworkInvoiceViewSet(viewsets.ModelViewSet):
    queryset = GSTJobworkInvoice.objects.all().order_by('-id')
    serializer_class = GSTJobworkInvoiceSerializer

    # Create Invoice
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "GST Jobwork Invoice created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update Invoice
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "GST Jobwork Invoice updated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete Invoice
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response(
            {
                "message": "GST Jobwork Invoice deleted successfully"
            },
            status=status.HTTP_204_NO_CONTENT
        )



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .utils import create_invoice_no


class GenerateGSTJobworkInvoiceNo(APIView):
    def get(self, request):
        try:
            invoice_no = create_invoice_no()
            return Response({"invoice_no": invoice_no},status=status.HTTP_200_OK)

        except ValueError as e:
            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import GSTJobworkRateDiff
from .serializers import GSTJobworkRateDiffSerializer


# Create + List API
class GSTJobworkRateDiffAPIView(APIView):

    def get(self, request):
        queryset = GSTJobworkRateDiff.objects.all().order_by('-id')
        serializer = GSTJobworkRateDiffSerializer(queryset, many=True)

        return Response({"message": "Data fetched successfully","data": serializer.data},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = GSTJobworkRateDiffSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response( {
                    "message": "GST Jobwork Rate Diff created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# Retrieve + Update + Delete API
class GSTJobworkRateDiffDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return GSTJobworkRateDiff.objects.get(pk=pk)
        except GSTJobworkRateDiff.DoesNotExist:
            return None

    def get(self, request, pk):
        obj = self.get_object(pk)

        if not obj:
            return Response(
                {"error": "Data not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = GSTJobworkRateDiffSerializer(obj)

        return Response(
            {
                "message": "Data fetched successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):
        obj = self.get_object(pk)

        if not obj:
            return Response(
                {"error": "Data not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = GSTJobworkRateDiffSerializer(
            obj,
            data=request.data
        )

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
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        obj = self.get_object(pk)

        if not obj:
            return Response(
                {"error": "Data not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        obj.delete()

        return Response(
            {
                "message": "Data deleted successfully"
            },
            status=status.HTTP_204_NO_CONTENT
        )
    


from .utils import create_debit_note_no_rate_diff

class GenerateGSTJobworkRateDiffDebitNoteNo(APIView):
    def get(self, request):
        try:
            debit_note_no = create_debit_note_no_rate_diff()

            return Response(
                {
                    "debit_note_no": debit_note_no
                },
                status=status.HTTP_200_OK
            )

        except ValueError as e:
            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GSTJobworkInvoiceFilterAPIView(APIView):

    def get(self, request):
        try:
            queryset = GSTJobworkInvoice.objects.all().order_by('-id')

            from_date = request.query_params.get("from_date")
            to_date = request.query_params.get("to_date")
            customer_name = request.query_params.get("customer_name")

            # Date range filter
            if from_date and to_date:
                queryset = queryset.filter(
                    invoice_date__range=[from_date, to_date]
                )

            # Customer name search
            if customer_name:
                queryset = queryset.filter(
                    bill_to_cust__icontains=customer_name
                )

            serializer = GSTJobworkInvoiceSerializer(queryset, many=True)

            return Response(
                {
                    "message": "Filtered invoices fetched successfully",
                    "count": queryset.count(),
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        

def generate_gstjobwork_invoice_pdf(request, pk):
    # Fetch invoice
    invoice = get_object_or_404(
        GSTJobworkInvoice.objects.prefetch_related('items').select_related('gst_details'),
        pk=pk
    )
    items = invoice.items.all()
    gst_details = getattr(invoice, 'gst_details', None)    
    grand_item_total = 0
    for item in items:
        try:
            qty = float(item.invoice_qty_kg or item.invoice_qty_nos or 0)
            rate = float(item.jobwork_rate or 0)

            item.amount = qty * rate
            grand_item_total += item.amount

        except:
            item.amount = 0

    context = {
        "invoice": invoice,
        "items": items,
        "gst_details": gst_details,
        "grand_item_total": grand_item_total
    }    
    template = get_template("Sales/gstjobwork_invoice_pdf.html")
    html = template.render(context)
    
    pdf_file = HTML(string=html).write_pdf()

    response = HttpResponse(
        pdf_file,
        content_type='application/pdf'
    )
    response['Content-Disposition'] = (
        f'inline; filename="GST_Invoice_{invoice.id}.pdf"'
    )
    return response




class CustomerPoAmendmentAPIView(APIView):
    def get(self, request):
        queryset = CustomerPoAmendment.objects.all().order_by('-amd_date')

        serializer = CustomerPoAmendmentSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomerPoAmendmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


from .utils import create_amd_no 
class GenerateCustomerPoAmdNo(APIView):
    def get(self, request):
        try:
            amd_no = create_amd_no()
            return Response(
                {"amd_no": amd_no},
                status=status.HTTP_200_OK
            )

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

from rest_framework.views import APIView
from rest_framework.response import Response
from collections import defaultdict
from Store.models import JobworkInwardChallanTable
# class ProductionByOutAndInPart(APIView):

#     def get(self, request):
#         out_part = request.query_params.get("out_part")

#         result = defaultdict(lambda: defaultdict(float))

#         item = None
#         operation = None
#         code_filter = None

#         # ================= PARSE =================
#         if out_part:
#             if "|" in out_part:
#                 # ✅ NORMAL FORMAT
#                 parts = [p.strip() for p in out_part.split("|")]

#                 item = parts[0].split("-")[0].strip()

#                 if len(parts) >= 3:
#                     operation = parts[2].strip()

#             elif "-" in out_part:
#                 # ✅ CODE FORMAT
#                 code_filter = out_part.strip()

#         # ================= PRODUCTION =================
#         entries = ProductionEntry.objects.all()

#         if item:
#             entries = entries.filter(item__icontains=item)

#         if operation:
#             entries = entries.filter(operation__icontains=operation)

#         # ❗ code_filter ka production me direct use nahi (no mapping)

#         for e in entries:
#             opno = (e.operation or "N/A").strip()
#             lot = (e.lot_no or "N/A").split("|")[0]
#             qty = safe_float(e.prod_qty)

#             result[opno][lot] += qty

#         # ================= GRN =================
#         grn_queryset = JobworkInwardChallanTable.objects.all()

#         if item:
#             grn_queryset = grn_queryset.filter(ItemCode__icontains=item)

#         # if operation:
#         #     grn_queryset = grn_queryset.filter(
#         #         ParticularNatureOfProcess__icontains=operation
#         #     )
#         if operation:
#             grn_queryset = grn_queryset.filter(
#                 FGPartCode__icontains=operation
#             )
#         if code_filter:
#             # ✅ MATCH FGPartCode like:
#             # PFFGFG1001-gr1FGFG1001
#             grn_queryset = grn_queryset.filter(
#                 FGPartCode__icontains=code_filter.split("-")[0]
#             )

#         for row in grn_queryset:
#             fg_part = row.FGPartCode or "N/A"
#             heat_no = row.HeatNo or "N/A"
#             grn_qty = safe_float(row.GRNQty)

#             parts = [p.strip() for p in fg_part.split("|")]

#             if len(parts) >= 2:
#                 op_key = f"{parts[0]}|{parts[1]}"
#             else:
#                 op_key = fg_part.strip()

#             result[op_key][heat_no] += grn_qty

#         return Response({
#             "item": item,
#             "operation": operation,
#             "code_filter": code_filter,
#             "data": result
#         })


def safe_float(value):
    try:
        return float(value)
    except:
        return 0.0


class ProductionByOutAndInPart(APIView):

    def get(self, request):
        out_part = request.query_params.get("out_part")

        result = defaultdict(lambda: defaultdict(float))

        item = None
        op_no = None

        # ================= PARSE =================
        if out_part:
            out_part = out_part.replace('"', '').strip()

            if "|" in out_part:
                parts = [p.strip() for p in out_part.split("|")]

                # ✅ ITEM
                item = parts[0].split("-")[0].strip()

                # ✅ OP NO (MOST IMPORTANT)
                if "OP:" in out_part:
                    try:
                        op_no = out_part.split("OP:")[1].split("|")[0].strip()
                    except:
                        pass

        # ================= PRODUCTION =================
        entries = ProductionEntry.objects.all()

        if item:
            entries = entries.filter(item__icontains=item)

        # ❗ OP filter not applied (no OP field in ProductionEntry)

        for e in entries:
            op = (e.operation or "N/A").strip()
            lot = (e.lot_no or "N/A").split("|")[0]
            qty = safe_float(e.prod_qty)

            result[op][lot] += qty

        # ================= GRN =================
        grn_queryset = JobworkInwardChallanTable.objects.all()

        if item:
            grn_queryset = grn_queryset.filter(ItemCode__icontains=item)

        # 🔥 MAIN FILTER (ONLY OP NO)
        if op_no:
            grn_queryset = grn_queryset.filter(
                FGPartCode__startswith=op_no
            )

        for row in grn_queryset:
            fg_part = row.FGPartCode or "N/A"
            heat_no = row.HeatNo or "N/A"
            grn_qty = safe_float(row.GRNQty)

            parts = [p.strip() for p in fg_part.split("|")]

            if len(parts) >= 2:
                key = f"{parts[0]}|{parts[1]}"
            else:
                key = fg_part.strip()

            result[key][heat_no] += grn_qty

        return Response({
            "item": item,
            "op_no": op_no,
            "data": result
        })
    




class CreditNoteAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                credit_note = CreditNote.objects.get(id=pk)
            except CreditNote.DoesNotExist:
                return Response(
                    {"message": "Credit Note not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = CreditNoteSerializer(credit_note)
            return Response(serializer.data)

        credit_notes = CreditNote.objects.all().order_by('-id')
        serializer = CreditNoteSerializer(credit_notes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CreditNoteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Credit Note created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            credit_note = CreditNote.objects.get(id=pk)
        except CreditNote.DoesNotExist:
            return Response(
                {"message": "Credit Note not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CreditNoteSerializer(
            credit_note,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Credit Note updated successfully",
                    "data": serializer.data
                }
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            credit_note = CreditNote.objects.get(id=pk)
        except CreditNote.DoesNotExist:
            return Response(
                {"message": "Credit Note not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        credit_note.delete()

        return Response(
            {"message": "Credit Note deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )




from .utils import create_credit_note_no
class GenerateCreditNoteNo(APIView):
    def get(self, request):
        try:
            credit_note_no = create_credit_note_no()

            return Response(
                {"credit_note_no": credit_note_no},
                status=status.HTTP_200_OK
            )

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# views.py

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from weasyprint import HTML
from .models import CreditNote


def generate_credit_note_pdf(request, pk):

    # Fetch Credit Note
    credit_note = get_object_or_404(
        CreditNote.objects.prefetch_related('items'),
        pk=pk
    )

    items = credit_note.items.all()

    # Grand Total Calculation
    grand_item_total = 0

    for item in items:
        try:
            qty = float(item.quntity or 0)
            rate = float(item.rate or 0)

            item.total_amount = qty * rate
            grand_item_total += item.total_amount

        except:
            item.total_amount = 0

    context = {
        "credit_note": credit_note,
        "items": items,
        "grand_item_total": grand_item_total,
    }

    template = get_template("Sales/credit_note_pdf.html")

    html = template.render(context)

    pdf = HTML(string=html).write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')

    response['Content-Disposition'] = (
        f'inline; filename="Credit_Note_{credit_note.id}.pdf"'
    )

    return response


# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import NewProfomaInvoice
from .serializers import NewProfomaInvoiceSerializer


class NewProfomaInvoiceAPIView(APIView):

    def get(self, request, pk=None):

        if pk:
            try:
                invoice = NewProfomaInvoice.objects.get(id=pk)
                serializer = NewProfomaInvoiceSerializer(invoice)
                return Response(serializer.data, status=status.HTTP_200_OK)

            except NewProfomaInvoice.DoesNotExist:
                return Response(
                    {"error": "Invoice not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

        invoices = NewProfomaInvoice.objects.all().order_by('-id')
        serializer = NewProfomaInvoiceSerializer(invoices, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = NewProfomaInvoiceSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Profoma Invoice Created Successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request, pk):
        try:
            invoice = NewProfomaInvoice.objects.get(id=pk)

        except NewProfomaInvoice.DoesNotExist:
            return Response(
                {"error": "Invoice not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = NewProfomaInvoiceSerializer(
            invoice,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Profoma Invoice Updated Successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        try:
            invoice = NewProfomaInvoice.objects.get(id=pk)

        except NewProfomaInvoice.DoesNotExist:
            return Response(
                {"error": "Invoice not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        invoice.delete()

        return Response(
            {"message": "Profoma Invoice Deleted Successfully"},
            status=status.HTTP_200_OK
        )
    

from .utils import create_invoice_no
class GenerateInvoiceNo(APIView):
    def get(self, request):
        try:
            invoice_no = create_invoice_no()

            return Response(
                {"invoice_no": invoice_no},
                status=status.HTTP_200_OK
            )

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


import re
from collections import defaultdict

from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from All_Masters.models import ItemTable, BOMItem
from Production.models import ProductionEntry
from Store.models import InwardChallanTable
from Quality.models import InwardtestQCinfo

def safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


class HeatAPIView(APIView):
    def get_qc_summary(self, fg_item):

        part_no = fg_item.part_no

        qc_summary = defaultdict(
            lambda: defaultdict(float)
        )

        qc_infos = InwardtestQCinfo.objects.filter(
            Q(item__icontains=part_no)
        )

        for qc in qc_infos:

            raw_op = (
                qc.opno or ""
            ).strip()

            if not raw_op:
                continue

            

            operation_no = (
                raw_op
                .split("|")[0]
                .strip()
            )

            match = re.search(
                r"\d+",
                operation_no
            )

            if not match:
                continue

            operation_no = match.group(0)

            heat = (
                qc.heat_no or ""
            ).strip()

            if not heat:
                continue

            qc_summary[
                operation_no
            ][heat] += safe_float(
                qc.ok_qty
            )

        return qc_summary


    def get_operation_number(self, operation):

        if not operation:
            return None

        operation = str(operation).strip()

        operation = operation.split("|")[0].strip()

        match = re.search(
            r"\d+",
            operation
        )

        if match:
            return match.group(0)

        return None

    def get_bom_operation_key(
        self,
        bom_items,
        operation_no
    ):

        if not operation_no:
            return None

        for bom in bom_items:

            bom_operation = str(
                bom.OPNo or ""
            ).strip()

            if not bom_operation:
                continue

            bom_operation_no = (
                self.get_operation_number(
                    bom_operation
                )
            )

            if bom_operation_no == operation_no:

                return bom_operation

        return None


    def get(self, request):

        search = request.query_params.get(
            "part_no",
            ""
        ).strip()


        if not search:

            return Response(
                {
                    "error": "part_no is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            fg_item = (
                ItemTable.objects
                .prefetch_related(
                    "bom_items"
                )
                .get(
                    Q(
                        part_no__iexact=search
                    )
                    |
                    Q(
                        Part_Code__iexact=search
                    )
                    |
                    Q(
                        Name_Description__iexact=search
                    )
                )
            )

        except ItemTable.DoesNotExist:

            return Response(
                {
                    "error": "FG Part not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        except ItemTable.MultipleObjectsReturned:

            return Response(
                {
                    "error": (
                        "Multiple FG items found. "
                        "Search using unique value."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        part_no = fg_item.part_no


        bom_items = list(
            BOMItem.objects
            .filter(
                item=fg_item
            )
            .order_by(
                "OPNo"
            )
        )

        if not bom_items:

            return Response(
                {},
                status=status.HTTP_200_OK
            )

        rm_part = None

        for bom in bom_items:

            operation_no = (
                self.get_operation_number(
                    bom.OPNo
                )
            )

            if operation_no == "10":

                rm_part = bom.BomPartCode

                break


        operation_summary = defaultdict(
            lambda: defaultdict(float)
        )

        inward_filter = Q()

        if rm_part:

            inward_filter |= Q(
                ItemDescription__startswith=rm_part
            )

        inward_filter |= Q(
            ItemDescription__contains=(
                f"Part: {part_no}"
            )
        )

        inwards = (
            InwardChallanTable.objects
            .filter(
                inward_filter
            )
        )

        for inward in inwards:

            item_desc = (
                inward.ItemDescription or ""
            ).strip()

            operation_no = None

            if (
                rm_part
                and
                item_desc.startswith(
                    rm_part
                )
            ):

                raw_op = (
                    inward.opno or ""
                ).strip()

                if not raw_op:
                    continue

 
                match = re.search(
                    r"OP\s*:?\s*(\d+)",
                    raw_op,
                    re.IGNORECASE
                )

                if match:

                    operation_no = (
                        match.group(1)
                    )

                else:

                    operation_no = (
                        self.get_operation_number(
                            raw_op
                        )
                    )

            elif (
                f"Part: {part_no}"
                in item_desc
            ):

                match = re.search(
                    r"Op:\s*OP:(\d+)",
                    item_desc,
                    re.IGNORECASE
                )

                if match:

                    operation_no = (
                        match.group(1)
                    )

            if not operation_no:
                continue

            operation_key = (
                self.get_bom_operation_key(
                    bom_items,
                    operation_no
                )
            )

            if not operation_key:
                continue


            heat = (
                inward.heat_no or ""
            ).strip()

            if not heat:
                continue

            qty = safe_float(
                inward.ChallanQty
            )

            operation_summary[
                operation_key
            ][heat] += qty


        productions = (
            ProductionEntry.objects
            .filter(
                Q(
                    ItemCode=part_no
                )
                |
                Q(
                    item__icontains=part_no
                )
            )
        )

        for prod in productions:


            operation_key = (
                prod.operation or ""
            ).strip()

            if not operation_key:
                continue

            operation_no = (
                self.get_operation_number(
                    operation_key
                )
            )

            if not operation_no:
                continue

            bom_operation_key = (
                self.get_bom_operation_key(
                    bom_items,
                    operation_no
                )
            )

            if not bom_operation_key:
                continue

            operation_key = operation_key


            heat = (
                prod.lot_no or ""
            ).split("|")[0].strip()

            if not heat:
                continue

 
            qty = safe_float(
                prod.prod_qty
            )

            operation_summary[
                operation_key
            ][heat] += qty


        qc_summary = (
            self.get_qc_summary(
                fg_item
            )
        )

 
        response = {}

 
        for operation_key, heat_data in (
            operation_summary.items()
        ):

            if not heat_data:
                continue


            operation_no = (
                self.get_operation_number(
                    operation_key
                )
            )

            if not operation_no:
                continue


            matching_bom = None

            for bom in bom_items:

                bom_operation_key = str(
                    bom.OPNo or ""
                ).strip()

                bom_operation_no = (
                    self.get_operation_number(
                        bom_operation_key
                    )
                )

                if (
                    bom_operation_no
                    == operation_no
                ):

                    matching_bom = bom

                    break

            if not matching_bom:
                continue

 
            qc_flag = bool(
                getattr(
                    matching_bom,
                    "QC",
                    False
                )
            )

    
            if qc_flag:

                for heat, qty in (
                    heat_data.items()
                ):

                    ok_qty = (
                        qc_summary
                        .get(
                            operation_no,
                            {}
                        )
                        .get(
                            heat,
                            0.0
                        )
                    )

 
                    if ok_qty <= 0:
                        continue

  
                    response.setdefault(
                        operation_key,
                        {}
                    )

                    response[
                        operation_key
                    ][heat] = min(
                        qty,
                        ok_qty
                    )

            else:

                response[
                    operation_key
                ] = dict(
                    heat_data
                )


        return Response(
            response,
            status=status.HTTP_200_OK
        )