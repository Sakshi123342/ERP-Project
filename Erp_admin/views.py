from rest_framework import generics
from rest_framework.permissions import AllowAny
from vendor.models import AdminModel
from .serializers import AdminModelRegisterSerializer, AdminModelLoginSerializer
from rest_framework.response import Response
from rest_framework import status

class AdminModelRegistration(generics.CreateAPIView):
    queryset = AdminModel.objects.all()
    serializer_class = AdminModelRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"message": "Bank registered successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)

class AdminModelLoginView(generics.GenericAPIView):
    serializer_class = AdminModelLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Login successful.", "data": serializer.validated_data}, status=status.HTTP_200_OK)
    

from .serializers import ModulePermissionSerializer
from vendor.models import AdminModel

class GeneralDetailsListCreate(generics.ListCreateAPIView):
    queryset = AdminModel.objects.all()
    serializer_class = ModulePermissionSerializer

class GeneralDetailsRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdminModel.objects.all()
    serializer_class = ModulePermissionSerializer