from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import ToolManagement
from .serializers import ToolManagementSerializer


class ToolManagementAPIView(APIView):

    # GET API
    def get(self, request):

        tool_data = ToolManagement.objects.all().order_by('-id')

        serializer = ToolManagementSerializer(tool_data, many=True)

        return Response({
            "status": True,
            "count": tool_data.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    # POST API
    def post(self, request):

        serializer = ToolManagementSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "status": True,
                "message": "Tool Management created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)