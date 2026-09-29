from rest_framework import serializers
from .models import *



class PendingBillGrnlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingBillGrnlist
        fields = '__all__'




class BillRegisterItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillRegisterItem
        fields = '__all__'


class BillRegisterSerializer(serializers.ModelSerializer):
    items = BillRegisterItemSerializer(many=True)

    class Meta:
        model = BillRegister
        fields = '__all__'

    def create(self, validated_data):
            items_data = validated_data.pop('items', [])

            # Parent Save
            bill_register = BillRegister.objects.create(**validated_data)

            # Child Save
            for item in items_data:
                BillRegisterItem.objects.create(
                    bill_register=bill_register,
                    **item
                )

            return bill_register
    

class JobworkBillRegisterItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = JobworkBillRegisterItem
        fields = '__all__'
        read_only_fields = ['bill_register']


class JobworkBillRegisterSerializer(serializers.ModelSerializer):
    items = JobworkBillRegisterItemSerializer(many=True)

    class Meta:
        model = JobworkBillRegister
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])

        bill_register = JobworkBillRegister.objects.create(**validated_data)

        for item_data in items_data:
            JobworkBillRegisterItem.objects.create(
                bill_register=bill_register,
                **item_data
            )

        return bill_register


class GeneralLedgerMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralLedgerMaster
        fields = '__all__'