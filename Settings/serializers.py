# serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from .models import MyModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user



# serializers.py
class MyModelSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(read_only=False, write_only=False)

    class Meta:
        model = MyModel
        fields = ['id', 'username', 'email', 'password', 'PlantName', 'Department', 'FullName', 'MobileNo']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        raw_password = validated_data.pop('password')

        print("PASSWORD RECEIVED:", raw_password)  # ✅ Debug line

        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=raw_password
        )

        my_model = MyModel.objects.create(
            user=user,
            password=raw_password,
            **validated_data
        )
        return my_model


    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        raw_password = validated_data.get('password')

        if 'username' in user_data:
            instance.user.username = user_data['username']
        if 'email' in user_data:
            instance.user.email = user_data['email']
        if raw_password:
            instance.user.set_password(raw_password)
            instance.password = raw_password

        instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance



# Creating FinancialYear
from rest_framework import serializers
from .models import FinancialYear

class FinancialYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialYear
        fields = ['id', 'FyName', 'From_Date', 'To_Date', 'ShortName']


# class ScheduleMonthSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ScheduleMonthMaster
#         fields = '__all__'

from Planning.serializers import ProductionScheduleSerializer
from Planning.models import ProductionSchedule
class ScheduleMonthSerializer(serializers.ModelSerializer):
    production_schedules = ProductionScheduleSerializer(many=True, required=False)

    class Meta:
        model = ScheduleMonthMaster
        fields = '__all__'

    def create(self, validated_data):
        schedules_data = validated_data.pop('production_schedules', [])  # 👈 fix
        month = ScheduleMonthMaster.objects.create(**validated_data)

        for schedule in schedules_data:
            ProductionSchedule.objects.create(
                schedule_month=month,
                **schedule
            )

        return month