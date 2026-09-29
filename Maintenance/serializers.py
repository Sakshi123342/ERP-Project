from rest_framework import serializers
from .models import *


class ToolManagementSerializer(serializers.ModelSerializer):

    class Meta:
        model = ToolManagement
        fields = '__all__'