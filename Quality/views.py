from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets
from .models import *
from .serializers import *
# Create your views here.



@api_view(['GET'])
def test_view(request):
    return Response({"message": "Quality is coming"})



from rest_framework.views import APIView
from rest_framework.response import Response
from Purchase.models import PurchasePO
from Purchase.serializers import OOPurchaseSerializer


class PurchasePOforInwardtestlist(APIView):

    def get(self, request):

        supplier = request.GET.get('supplier')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        queryset = PurchasePO.objects.prefetch_related(
            'Item_Detail_Enter',
            'Gst_Details',
            'Item_Details_Other',
            'Schedule_Line',
            'Ship_To_Add'
        ).all().order_by('-PoDate')

        if supplier:
            queryset = queryset.filter(Supplier__icontains=supplier)

        if start_date and end_date:
            queryset = queryset.filter(PoDate__range=[start_date, end_date])

        serializer =OOPurchaseSerializer(queryset, many=True)

        return Response({
            "count": queryset.count(),
            "results": serializer.data
        })



from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import (
    InwardtestQCinfo,
    InwardtestDimensional,
    Inwardtestvisulainspection,
    InwardtestreworkQty,
    InwardtestrejectQty
)
from .serializers import InwardtestQCinfoSerializer


class InwardtestQCinfoViewSet(viewsets.ModelViewSet):

    queryset = InwardtestQCinfo.objects.all().order_by('-id')
    serializer_class = InwardtestQCinfoSerializer


    # CREATE
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "status": True,
            "message": "QC Info created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


    # LIST
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            "status": True,
            "data": serializer.data
        })


    # RETRIEVE SINGLE
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({
            "status": True,
            "data": serializer.data
        })


    # UPDATE
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "status": True,
            "message": "QC Info updated successfully",
            "data": serializer.data
        })


    # DELETE
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response({
            "status": True,
            "message": "QC Info deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)
    



class SubconJobworkQCInfoListCreateView(APIView):
   
    def get(self, request):
        qc = SubconJobworkQCInfo.objects.all().order_by('-id')
        serializer = SubconJobworkQCInfoSerializer(qc, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubconJobworkQCInfoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "QC Created Successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class SubconJobworkQCInfoDetailView(APIView):   
    def get(self, request, pk):
        qc = get_object_or_404(SubconJobworkQCInfo, pk=pk)
        serializer = SubconJobworkQCInfoSerializer(qc)
        return Response(serializer.data)

    def put(self, request, pk):
        qc = get_object_or_404(SubconJobworkQCInfo, pk=pk)

        serializer = SubconJobworkQCInfoSerializer(
            qc,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "QC Updated Successfully",
                "data": serializer.data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # PATCH partial update
    def patch(self, request, pk):
        qc = get_object_or_404(SubconJobworkQCInfo, pk=pk)

        serializer = SubconJobworkQCInfoSerializer(
            qc,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "QC Updated Successfully",
                "data": serializer.data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # DELETE record
    def delete(self, request, pk):
        qc = get_object_or_404(SubconJobworkQCInfo, pk=pk)
        qc.delete()

        return Response({
            "message": "QC Deleted Successfully"
        }, status=status.HTTP_204_NO_CONTENT)
    





class SalesReturnQcInfoAPI(APIView):

    def get(self, request):

        data = SalesReturnQcInfo.objects.all().order_by('-id')

        serializer = SalesReturnQcInfoSerializer(data, many=True)

        return Response(serializer.data)


    def post(self, request):

        serializer = SalesReturnQcInfoSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                {"message": "Sales Return QC Created Successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


from .utils import generate_qc_number
class GenerateUniqueQcNumber(APIView):
    
    def get(self, request):
        try:
            qc_no = generate_qc_number()
            
            return Response(
                {"qc_no": qc_no},
                status=status.HTTP_200_OK
            )
        
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
from .utils import subcon_genrate_qc_no
class GenrateSubconQcNo(APIView):
    def get(self , request):
        try:
            qc= subcon_genrate_qc_no()
            return Response({"qc":qc},status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
from .utils import Inwardtedt_generate_qc_no
class GenrateInwardTestqcno(APIView):
    def get(self , request):
        try:
            qc_no= Inwardtedt_generate_qc_no()
            return Response({"qc_no":qc_no},status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)








import re
from rest_framework import generics
from rest_framework.response import Response
from Store.models import InwardChallan2
from All_Masters.models import BOMItem
from Store.serializers import InwardChallanSerializer


# class FilteredInwardChallanAPI(generics.ListAPIView):
#     serializer_class = InwardChallanSerializer

#     def get_queryset(self):
#         inward_qs = InwardChallan2.objects.all()
#         filtered_ids = []

#         for inward in inward_qs:
#             challan_items = inward.InwardChallanTable.all()

#             for item in challan_items:
#                 desc = item.ItemDescription or ""

#                 # 🔍 Extract OP number (e.g., OP:20)
#                 match = re.search(r'Op:\s*OP:(\d+)', desc)
#                 if match:
#                     op_no = match.group(1)

#                     # 🔍 Get Item (based on your logic, adjust if needed)
#                     # Example: match using part code from description
#                     part_match = re.search(r'Part:\s*(\w+)', desc)
#                     if part_match:
#                         part_code = part_match.group(1)

#                         # Find BOM items
#                         bom_items = BOMItem.objects.filter(
#                             item__part_no=part_code,
#                             OPNo=op_no,
#                              QC=True  
#                         )

#                         # for bom in bom_items:
#                         #     if str(bom.QC).lower() in ["1", "Yes"]:
#                         #         filtered_ids.append(inward.id)
#                         #         break
#                         if bom_items.exists():
#                             filtered_ids.append(inward.id)
#                             break

#         return InwardChallan2.objects.filter(id__in=filtered_ids)

class FilteredInwardChallanAPI(generics.ListAPIView):
    serializer_class = InwardChallanSerializer

    def get_queryset(self):
        inward_qs = InwardChallan2.objects.prefetch_related("InwardChallanTable")
        filtered_ids = set()

        for inward in inward_qs:
            for item in inward.InwardChallanTable.all():
                desc = item.ItemDescription or ""

                # Extract OP number
                match = re.search(r'OP:(\d+)', desc)
                if not match:
                    continue
                op_no = match.group(1)

                # Extract Part Code
                part_match = re.search(r'Part:\s*(\w+)', desc)
                if not part_match:
                    continue
                part_code = part_match.group(1)

                # Check BOM with QC=True
                if BOMItem.objects.filter(
                    item__part_no=part_code,
                    OPNo=op_no,
                    QC=True
                ).exists():
                    filtered_ids.add(inward.id)
                    break  # stop checking more items for this inward

        return InwardChallan2.objects.filter(id__in=filtered_ids)



from rest_framework.views import APIView
from rest_framework.response import Response
from All_Masters.models import ItemTable, BOMItem
from Production.models import ProductionEntry
from Production.serializers import ProductionEntrySerializer


# class QCProductionEntryAPIView(APIView):
#     """
#     Return only those Production Entries whose Operation
#     has QC=True in BOM.
#     """

#     def get(self, request):
#         production_entries = ProductionEntry.objects.all().order_by("-id")
#         result = []

#         for entry in production_entries:
#             try:
#                 # Example:
#                 # item = "FGFG1006 | Toll | CoilPart"
#                 item_part_no = entry.item.split("|")[0].strip()

#                 item_obj = ItemTable.objects.get(part_no=item_part_no)

#                 # Example:
#                 # operation = "10|chFGFG1006"
#                 operation_data = entry.operation.split("|")

#                 if len(operation_data) < 2:
#                     continue

#                 op_no = operation_data[0].strip()
#                 part_code = operation_data[1].strip()

#                 bom_exists = BOMItem.objects.filter(
#                     item=item_obj,
#                     OPNo=op_no,
#                     PartCode=part_code,
#                     QC=True
#                 ).exists()

#                 if bom_exists:
#                     result.append(entry)

#             except ItemTable.DoesNotExist:
#                 continue

#             except ItemTable.MultipleObjectsReturned:
#                 # Skip duplicate ItemTable records
#                 continue

#             except Exception:
#                 continue

#         serializer = ProductionEntrySerializer(result, many=True)
#         return Response(serializer.data)




from rest_framework.views import APIView
from rest_framework.response import Response

from All_Masters.models import ItemTable, BOMItem
from Production.models import ProductionEntry
from Production.serializers import ProductionEntrySerializer
from .models import InwardtestQCinfo


class QCProductionEntryAPIView(APIView):
    """
    Return only those Production Entries:

    1. Whose Operation has QC=True in BOM.
    2. Whose Prod_no is NOT already present in InwardtestQCinfo.
    """

    def get(self, request):

        existing_qc_prod_nos = set(
            InwardtestQCinfo.objects
            .exclude(prod_no__isnull=True)
            .exclude(prod_no="")
            .values_list("prod_no", flat=True)
        )

        production_entries = (
            ProductionEntry.objects
            .all()
            .order_by("-id")
        )

        result = []

        for entry in production_entries:

            try:
                
                if entry.Prod_no in existing_qc_prod_nos:
                    continue


                if not entry.item:
                    continue

                item_part_no = entry.item.split("|")[0].strip()

                item_obj = ItemTable.objects.get(
                    part_no=item_part_no
                )


                if not entry.operation:
                    continue

                operation_data = entry.operation.split("|")

                if len(operation_data) < 2:
                    continue

                op_no = operation_data[0].strip()
                part_code = operation_data[1].strip()

                bom_exists = BOMItem.objects.filter(
                    item=item_obj,
                    OPNo=op_no,
                    PartCode=part_code,
                    QC=True
                ).exists()

                if not bom_exists:
                    continue
                result.append(entry)

            except ItemTable.DoesNotExist:
                continue

            except ItemTable.MultipleObjectsReturned:
                continue

            except Exception:
                continue

        serializer = ProductionEntrySerializer(
            result,
            many=True
        )

        return Response(serializer.data)

