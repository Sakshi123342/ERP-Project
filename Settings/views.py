# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import MyModel
from .serializers import MyModelSerializer

# Register a new user
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import MyModel

@api_view(['POST'])
def register_user(request):

    required_fields = ['username', 'email', 'password', 'PlantName', 'Department', 'FullName', 'MobileNo']
    
    for field in required_fields:
        if field not in request.data:
            return Response({"error": f"'{field}' is required."}, status=status.HTTP_400_BAD_REQUEST)

    username = request.data['username']
    email = request.data['email']
    password = request.data['password']

    if User.objects.filter(email=email).exists():
        return Response({"error": "This email is already registered."}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({"error": "This username is already taken."}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    # ✅ Add password in MyModel too!
    MyModel.objects.create(
        user=user,
        password=password,  # ← this was missing!
        PlantName=request.data['PlantName'],
        Department=request.data['Department'],
        FullName=request.data['FullName'],
        MobileNo=request.data['MobileNo']
    )

    return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)



# Get all users or single user by id
@api_view(['GET'])
def get_users(request, pk=None):
    if pk:
        try:
            user = MyModel.objects.get(pk=pk)
            serializer = MyModelSerializer(user)
            return Response(serializer.data)
        except MyModel.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    else:
        users = MyModel.objects.all()
        serializer = MyModelSerializer(users, many=True)
        return Response(serializer.data)

# Get list of users for dropdown
@api_view(['GET'])
def get_users_for_dropdown(request):
    users = MyModel.objects.all().values('id', 'FullName')  # Only return id and FullName
    return Response(users)


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MyModel
from .serializers import MyModelSerializer

class UserDetailView(APIView):
    def get(self, request, pk):
        try:
            user = MyModel.objects.get(pk=pk)
            serializer = MyModelSerializer(user)
            return Response(serializer.data)
        except MyModel.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            user = MyModel.objects.get(pk=pk)
            user.delete()
            return Response({"detail": "Deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except MyModel.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)


from rest_framework import viewsets
from .models import MyModel
from .serializers import MyModelSerializer

class MyModelViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()  # Get all registered users
    serializer_class = MyModelSerializer

# models.py (Assuming you have a Module model)



# views.py
from .models import MyModel, UserPermission, Module
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import MyModel, Module, UserPermission
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def assign_permissions(request):
    user_id = request.data.get('id')
    modules = request.data.get('modules', {})  # Dictionary: { "ModuleName": ["Page1", "Page2"] }
    print("Request Data:", request.data)
    print("User ID:", user_id)
    print("Modules:", modules)
    if not user_id:
        return Response({"message": "id is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_instance = MyModel.objects.get(id=user_id)
    except MyModel.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Clear previous permissions
    UserPermission.objects.filter(user=user_instance).delete()

    assigned_permissions = {}
    errors = []

    for module_name, pages in modules.items():
        assigned_pages = set()

        for page_name in pages:
            try:
                # Here, module is actually page name based on your setup
                module_instance, _ = Module.objects.get_or_create(name=page_name)
                UserPermission.objects.create(user=user_instance, module=module_instance)
                assigned_pages.add(page_name)
            except Exception as e:
                print("ERROR:", repr(e))
                errors.append(f"Error assigning '{page_name}' under '{module_name}': {str(e)}")

        if assigned_pages:
            assigned_permissions[module_name] = list(assigned_pages)

    if errors:
        return Response({
            "message": "Some permissions were not assigned due to errors",
            "errors": errors,
            "assigned_permissions": assigned_permissions
        }, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        "message": "Permissions assigned successfully",
        "assigned_permissions": assigned_permissions
    }, status=status.HTTP_201_CREATED)


# LOGIN ERP
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from .models import MyModel, FinancialYear, UserPermission

@api_view(['POST'])
def login_user(request):
    username_or_email = request.data.get('username')
    password = request.data.get('password')
    year = request.data.get('year')

    if not username_or_email or not password or not year:
        return Response({"message": "Username, password, and year are required"}, status=status.HTTP_400_BAD_REQUEST)

    # ✅ Get User by username or email
    try:
        user = User.objects.get(username=username_or_email)
    except User.DoesNotExist:
        try:
            user = User.objects.get(email=username_or_email)
        except User.DoesNotExist:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    # ✅ Check password
    if not user.check_password(password):
        return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    # ✅ Get related MyModel instance
    try:
        my_model = MyModel.objects.get(user=user)
    except MyModel.DoesNotExist:
        return Response({"message": "User profile not found."}, status=status.HTTP_400_BAD_REQUEST)

    # ✅ JWT token generation
    refresh = RefreshToken.for_user(user)

    # ✅ Financial year check
    financial_years = FinancialYear.objects.filter(ShortName=year)
    if not financial_years.exists():
        return Response({"message": "Financial year not found"}, status=status.HTTP_404_NOT_FOUND)

    financial_year = financial_years.first()
    start_year, end_year = year.split('-')
    shortyear = start_year[2:4] + end_year[2:4]

    # ✅ Permissions based on MyModel
    user_permissions = UserPermission.objects.filter(user=my_model)
    permissions = {
        "All_Masters": set(),
        "Purchase": set(),
        "Store": set(),
        "Production": set(),
        "ERPSetting": set(),
        "VendorsUserManagement": set(),
        "Quality": set(),
        "Sales": set(),
        "Accounts": set(),
        "Maintenance": set(),
        "Dashboard": set(),
        "ProductionV2": set(),
    }

    # Group pages by modules (use your logic here)
    for permission in user_permissions:
        page_name = permission.module.name

        # Group logic — use your original logic here
        if page_name in ["Masters", "Customer", "Business Partner Address", "Item Master", "Cross Reference", "Customer / Supplier Item Link", "Item Cross Reference", "GST Rate Master", 
                             "Commodity Master", "BOM Routing Master", "Work Center Master", "Cycle Time Master", 
                             "Operator and Supervisor Master", "Contractor Master", "Shift Master", "Work Center Schedule", 
                             "Unit Conversion", "Price List", "Price List Master", "Price List Entry", "Cost Center Master", "Project Management", 
                             "Document Management", "Master Report", "Customer State", "Master Customers", "Master State"]:
                permissions["All_Masters"].add(page_name)

            # Handle Purchase pages (just add "Report" normally)
        if page_name in ["Purchase", "New Indent", "New Purchase Order", "New Jobwork Purchase Order", "Pending PO Release", 
                             "Pending Indent Release", "Purchase MRN Release", "Purchase Order Status", "Quote Comparison", "RFO", "Quoto Comparison Statement", "Quoto Comparison Pending",
                             "Reports", "Purchase Order List", "Jobwork Purchase Order List", "Supplier Wise Item Purchase List", "Purchase Report (Cost Center Wise)", "Import"]:
                permissions["Purchase"].add(page_name)

            # Handle Store pages
        if page_name in ["Store", "Gate Inward Entry", "Pending ASN List", "New MRN", "Purchase GRN", "Subcon GRN", "57F4 Inward Challan", "JobWork Inward Challan", "Vendor Scrap Inward", 
                             "Material Issue Challan", "Material Issue Gernal", "Stock Transaction", "Opening Stock", "FG Movement", "RM Stock Transaction", "Stock Transfer", "Delivery Challan", 
                             "DC GRN", "Store Report", "GRN List", "MRN List", "Inward 57F4 Challan List", "Material Issue Challan List", "General Material Issue Challan List", "Deliver Challan List", "DC GRN List",
                               "Indent List","Newindent" ,"Indent Status", "Stock Report", "WIP Stock Report", "RM Stock Report", "Consumable Stock Report", "FG Stock Report","SubcontractStock"]:
                permissions["Store"].add(page_name)

            # Handle Production pages (just add "Report" normally)
        if page_name in ["Production", "Work Order Entry", "Work Order List", "Production Plan List", "Production Entry",
                              "Production Entry Ass.", "Rework Production", "Rework Production Entry2", "Rework Production Entry", "Rework Production Report", 
                                "Scrap Production", "Scrap/Rejection Entry", "Scrap/Rejection Report", "FG Scrap/Rejection Entry", "FG Scrap/Rejection Report", "Material Idle Time", "Breakdown Time Entry",
                                  "Breakdown Time Report", "Contractor Payment", "P Report", "Production Ass Report", "Production Report", "Rejection Report", "Rework Report", "Default Ideal Time Report", "Breakdown Analysis Report", "Cycle Time Report", "Operator Performance Report"]:
                permissions["Production"].add(page_name)

            # Handle ERPSetting pages
        if page_name in ["ERPSetting", "User Configuration", "ERP Configuration", "Change Password",
                              "Login History", "Dealer Management", "Dashboard Backup",
                                "Delete Record"]:
                permissions["ERPSetting"].add(page_name)

            # Handle Sales pages (just add "Report" normally)
        if page_name in ["Sales", "E-Invoicing", "GST Sales", "JobWork Sales", "Debit Note",
                              "Credit Note", "Customer Sales Order", "Customer Sales Order Amendment",
                                "Schedule Sales Order", "Customer Sales Order Status", "GST Invoice",
                                  "GST JobWork", "GST JobWork Invoice", "GST JobWork DC Return", 
                                  "OutWard 57F4 Challan", "Credit / Debit Note", "Purchase Debit Note",
                                    "Sales Rate Diff Debit Note", "JobWork Rate Diff Debit Note", 
                                    "Credit Note Entry", "GST Sales Return", "Material GatePass",
                                      "Material GatePass New", "Pending Material GatePass", 
                                      "Material GatePass List", "Sales Report", "Customer Sales Order List", 
                                      "Tax Invoice List", "Tax Invoice List Bajaj", "JobWork Invoice List", 
                                      "JobWork DC List", "OutWard 57F4 Challan List", "Debit Note List", 
                                      "Credit Note List", "GST Sales Return List", "RG1 Register", "Transport List","NewProformaInvoice"]:
                permissions["Sales"].add(page_name)

            # Handle Quality pages
        if page_name in ["Quality", "Quality Planning", "Purchase GRN QC", "Pending QC List", 
                              "Inward Test Certificate", "Subcon / JobWork GRN QC", "Pending QC Inward",
                                "Inward Inspection List", "Inprocess QC", "Inprocess Inspection",
                                  "Inprocess Inspection List", "Sales Return QC", "Sales Return QC Pending List", 
                                  "Sales Return QC List", "Gauges And Instruction Calibration", "Heat Code Register",
                                    "DTC - Dispatch Test Certificate", "PDI - Pre Dispatch Inspection", 
                                    "First Piece Approval", "Set Up Approval", "Hot Inspection", "Sampling Plan",
                                      "Customer Complaint", "Customer Complaint Entry", "Customer Complaint Authorization",
                                        "Customer Complaint List", "Test Master", "Test Report", "Test Master",
                                          "Test Master List"]:
                permissions["Quality"].add(page_name)
        
        # Handle Production V2 pages
        if page_name in [
            "Production v2",
            "Work Order Entry V2",
            "Work Order Report V2",
            "Contract Work Order",
            "Contract Work Order Entry",
            "Contract Work Order List",
            "Work Order status entry",
            "Punching and laser schedule",
            "Punching program",
            "Power press",
        ]:
            permissions["ProductionV2"].add(page_name)
            
        # Handle Accounts pages
        if page_name in [
            "Accounts","GL Master",
            "Bill Passing",
            "Purchase Bill",
            "Jobwork Bill",
            "Direct Bill",
            "Purchase Register",
            "TDS Register",
            "TCS Register",
            "AC",
            "Tax Invoice List",
            "Jobwork Invoice List",
            "Debit Note List",
            "Credit Note List",
            "GST Sales Return List",
            "GL Ledger",
            "GST Report",
            "GSTR1",
            "HSN/SAC Summary",
            "GSTR 2",
            "GSTR 3B",
            "GSTR ITC_04"
        ]:
            permissions["Accounts"].add(page_name)

        # Handle Maintenance pages
        if page_name in [
            "Maintenance",
            "Asset List",
            "Item Asset Master",
            "Machine Breakdown",
            "Breakdown List",
            "Breakdown Authorisation",
            "Breakdown Report",
            "Breakdown Slip",
            "Machine Repair",
            "Repair Entry",
            "Repair List",
            "Machine Preventive",
            "Machine Preventive Entry",
            "Machine Preventive Report",
            "Machine Preventive Schedule",
            "Machine Preventive Setup",
            "Tool Management"
        ]:
            permissions["Maintenance"].add(page_name)
            
        # Handle Dashboard pages
        if page_name in [
            "Dashboard",

            # Financial
            "Financial",
            "Alerts",
            "Total Records",

            # Sales Dashboard
            "Sales and Purchase",
            "Daily Sales",
            "Monthly Sales",
            "Top 5 Sales Customer",
            "Top 5 Sales Item",
            "Item Wise Dispatch",
            "Business Plan",
            "State Wise Sales",

            # Purchase Dashboard
            "Monthly Purchase",
            "Daily Purchase",
            "Purchase Orders",
            "Top 5 Suppliers",
            "Top 5 Purchase Items",
            "GRN Value Summary",
            "GRN Value Details",
            "Supplier Rating Summary",

            # Store Dashboard
            "Favorite Item Stock",
            "Min/Max Levels",
            "Inward Stock Distribution",
            "Outward Stock Distribution",
            "Material Issue Challan",
            "Item Wise Stock Report",

             # Quality Dashboard
            "Trend Of Rejection % At Operation Level",
                "Item Wise Reject",
                "Item Wise Rework",
                "Scrap Value Report",
                "Sales Return Customer",
        ]:
            permissions["Dashboard"].add(page_name)

            # Handle Vendors User Management
        if page_name in ["VendorsUserManagement"]:
                permissions["VendorsUserManagement"].add(page_name)

        # ... (rest same as your logic)

    # ✅ Final Response
    refresh = RefreshToken.for_user(user)

    access_token = str(refresh.access_token)
    refresh_token = str(refresh)
    print("Access Token:", access_token)
    print("Refresh Token:", refresh_token)
    
    return Response({
        "message": "Login successful",
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        
        "username": user.username,
        "year": financial_year.ShortName,
        "Shortyear": shortyear,
        
        "permissions": {key: list(value) for key, value in permissions.items()}
        
        
    })




# Creating FinancialYear
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FinancialYear
from .serializers import FinancialYearSerializer

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def financial_years(request, pk=None):
    # For GET request (retrieve all or single FinancialYear)
    if request.method == 'GET':
        if pk:  # If a pk is provided, return the specific FinancialYear
            try:
                financial_year = FinancialYear.objects.get(pk=pk)
                serializer = FinancialYearSerializer(financial_year)
                return Response(serializer.data)
            except FinancialYear.DoesNotExist:
                return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:  # If no pk, return the list of all FinancialYears
            financial_years = FinancialYear.objects.all()
            serializer = FinancialYearSerializer(financial_years, many=True)
            return Response(serializer.data)

    # For POST request (create a new FinancialYear)
    elif request.method == 'POST':
        serializer = FinancialYearSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # For PUT request (update an existing FinancialYear)
    elif request.method == 'PUT':
        try:
            financial_year = FinancialYear.objects.get(pk=pk)
        except FinancialYear.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = FinancialYearSerializer(financial_year, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # For DELETE request (delete a specific FinancialYear)
    elif request.method == 'DELETE':
        try:
            financial_year = FinancialYear.objects.get(pk=pk)
        except FinancialYear.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        financial_year.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from .models import *
# from .serializers import *

# class ScheduleMonthAPIView(APIView):
    
#     def get(self, request):
#         queryset = ScheduleMonthMaster.objects.filter(user=request.user).order_by('-id')

#         data = []
#         for obj in queryset:
#             data.append({
#                 "id": obj.id,
#                 "month_name": obj.month_name,
#                 "from_date": obj.from_date,
#                 "to_date": obj.to_date,
#                 "month_no": obj.month_no,
#                 "year_no": obj.year_no,
#                 "w_days": obj.w_days,
#                 "username": obj.user.username   # ✅ login user name
#             })

#         return Response(data)

#     def post(self, request):
#         data = request.data.copy()
#         data['user'] = request.user.id   # ✅ login user auto assign

#         serializer = ScheduleMonthSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "message": "Created successfully",
#                 "data": serializer.data,
#                 "username": request.user.username  # ✅ extra show
#             }, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import ScheduleMonthMaster
from .serializers import ScheduleMonthSerializer


class ScheduleMonthAPIView(APIView):

    # ✅ GET (All data)
    def get(self, request,pk=None):
        queryset = ScheduleMonthMaster.objects.all().order_by('-id')
        serializer = ScheduleMonthSerializer(queryset, many=True)

        return Response({
            "message": "Data fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


    # ✅ POST (Create - user manually pass hoga)
    def post(self, request):
        serializer = ScheduleMonthSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # ✅ PUT (Update by ID)
    def put(self, request, pk):
        obj = get_object_or_404(ScheduleMonthMaster, pk=pk)

        serializer = ScheduleMonthSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # ✅ DELETE (Delete by ID)
    def delete(self, request, pk):
        obj = get_object_or_404(ScheduleMonthMaster, pk=pk)
        obj.delete()

        return Response({
            "message": "Deleted successfully"
        }, status=status.HTTP_200_OK)