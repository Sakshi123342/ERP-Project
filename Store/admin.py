from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(InwardChallan2)
admin.site.register(InwardChallanTable)
admin.site.register(GeneralDetails)
admin.site.register(ItemDetails)
admin.site.register(NewMrn)
admin.site.register(NewMRNTable)
admin.site.register(GrnGenralDetail)
admin.site.register(NewGrnList)
admin.site.register(GrnGst)
admin.site.register(GrnGstTDC)
admin.site.register(RefTC)
admin.site.register(Job_Work)
admin.site.register(VendorScrap)
admin.site.register(MaterialIssue)
admin.site.register(Material_Issue_General)
admin.site.register(DeliveryChallan)
admin.site.register(SecondDeliveryChallan)
admin.site.register(DC_GRN)
admin.site.register(MainGroup)
admin.site.register(ItemGroup)
admin.site.register(ItemTable)
admin.site.register(MaterialChallan)
admin.site.register(MaterialChallanTable)
admin.site.register(NewDCgrn)
admin.site.register(NewDCgrnTable)
admin.site.register(InwardChallanGSTDetails)
admin.site.register(JobworkInwardChallan)
admin.site.register(JobworkInwardChallanTable)



@admin.register(FGMovement)
class FGMovementAdmin(admin.ModelAdmin):
    list_display = [
        'trn_no', 'date', 'fg_item_code', 'fg_item_name', 
        'ok_qty', 'rework_qty', 'reject_qty', 'created_by', 'created_at'
    ]
    list_filter = ['date', 'stock_view', 'created_at']
    search_fields = ['trn_no', 'fg_item_code', 'fg_item_name', 'heat_code']
    readonly_fields = ['trn_no', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Transaction Info', {
            'fields': ('trn_no', 'date')
        }),
        ('Item Details', {
            'fields': ('fg_item_code', 'fg_item_name', 'fg_item_description')
        }),
        ('Operation & Quantities', {
            'fields': ('operation', 'ok_qty', 'rework_qty', 'reject_qty')
        }),
        ('Additional Info', {
            'fields': ('heat_code', 'stock_view', 'remark')
        }),
        ('System Info', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
