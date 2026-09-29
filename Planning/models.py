from django.db import models

# Create your models here.

from Settings.models import ScheduleMonthMaster
class ProductionSchedule(models.Model):
    schedule_month = models.ForeignKey(ScheduleMonthMaster,on_delete=models.CASCADE, related_name="production_schedules",blank=True,null=True            )
    rev_no = models.CharField(max_length=3000,blank=True,null=True)
    customer_name = models.CharField(max_length=3000,blank=True,null=True)
    so_no_date = models.DateField(blank=True,null=True)
    po_no_date = models.DateField(blank=True,null=True)
    schedule_no = models.CharField(max_length=3000,blank=True,null=True)
    item_no = models.CharField(max_length=3000,blank=True,null=True)
    item_code = models.CharField(max_length=3000,blank=True,null=True)
    item_description = models.CharField(max_length=3000,blank=True,null=True)
    sch_rec_on = models.DateField(blank=True,null=True)
    sch_qty = models.CharField(max_length=3000,blank=True,null=True)
    buffer_qty = models.CharField(max_length=3000,blank=True,null=True)
    next_month_sc =models.CharField(max_length=3000,blank=True,null=True)
    due_dispatch_date = models.DateField(blank=True,null=True)

class UpdateItemWiseMinMax(models.Model):
    item_no = models.CharField(max_length=500,blank=True,null=True)
    item_code = models.CharField(max_length=500,blank=True,null=True)
    description = models.CharField(max_length=500,blank=True,null=True)
    item_groups = models.CharField(max_length=500,blank=True,null=True)
    main_groups = models.CharField(max_length=500 ,blank=True,null=True)
    unit = models.CharField(max_length=500,blank=True,null=True)
    tariff_no = models.CharField(max_length=500 , blank=True,null=True)
    min_level = models.DecimalField(max_digits=50,decimal_places=2,blank=True,null=True)
    re_order_level = models.DecimalField(max_digits=50,decimal_places=2,blank=True,null=True)
    max_level = models.DecimalField(max_digits=50,decimal_places=2,blank=True,null=True)
    min_order = models.DecimalField(max_digits=50,decimal_places=2,blank=True,null=True)
    max_order = models.DecimalField(max_digits=50,decimal_places=2,blank=True,null=True)
    grn_tol_sub = models.DecimalField(max_digits=50,decimal_places=2,blank=True,null=True)
    grn_tol_add = models.DecimalField(max_digits=50,decimal_places=2,blank=True,null=True)
    user = models.CharField(max_length=500,blank=True,null=True)

class DispatchPlan(models.Model):
    plan_date = models.DateField(blank=True,null=True)
    customer_name = models.CharField(max_length=500,blank=True,null=True)
    item = models.CharField(max_length=500,blank=True,null=True)
    stock = models.CharField(max_length=500,blank=True,null=True)
    plan_quantity = models.CharField(max_length=500,blank=True,null=True)
    heat_code = models.CharField(max_length=500,blank=True,null=True)
    heat_no = models.CharField(max_length=500,blank=True,null=True)
    cust_ref_challan_no = models.CharField(max_length=500,blank=True,null=True)
    po_no = models.CharField(max_length=500,blank=True,null=True)
    select_material = models.CharField(max_length=500,blank=True,null=True)
    machine = models.CharField(max_length=500,blank=True,null=True)
    die_no = models.CharField(max_length=500,blank=True,null=True)
    material = models.TextField(blank=True,null=True)
    weigth = models.CharField(max_length=500,blank=True,null=True)
    tray_weigth = models.CharField(max_length=500,blank=True,null=True)
    dept_ppc = models.CharField(max_length=500,blank=True,null=True)
    dept_cc = models.CharField(max_length=500,blank=True,null=True)
    optional_fields = models.BooleanField(default=False,blank=True)
    remark = models.TextField(blank=True,null=True)




