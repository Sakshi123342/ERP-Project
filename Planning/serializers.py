from rest_framework import serializers
from .models import *




class ProductionScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionSchedule
        fields = '__all__'


class UpdateItemWiseMinMaxSerializer(serializers.ModelSerializer):

    class Meta:
        model = UpdateItemWiseMinMax
        fields = '__all__'


class DispatchPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = DispatchPlan
        fields = '__all__'


from All_Masters.models import Item       
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"
