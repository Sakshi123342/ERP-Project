from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *


# =========================
# Inward QC
# =========================

class InwardtestDimensionalInline(admin.TabularInline):
    model = InwardtestDimensional
    extra = 1

class InwardtestVisualInline(admin.TabularInline):
    model = Inwardtestvisulainspection
    extra = 1

class InwardtestReworkInline(admin.TabularInline):
    model = InwardtestreworkQty
    extra = 1

class InwardtestRejectInline(admin.TabularInline):
    model = InwardtestrejectQty
    extra = 1


@admin.register(InwardtestQCinfo)
class InwardtestQCinfoAdmin(admin.ModelAdmin):
    list_display = ('qc_no', 'date', 'qc_time', 'ok_qty', 'approved_by')
    search_fields = ('qc_no', 'approved_by')
    list_filter = ('date',)
    inlines = [
        InwardtestDimensionalInline,
        InwardtestVisualInline,
        InwardtestReworkInline,
        InwardtestRejectInline
    ]


# =========================
# Subcon Jobwork QC
# =========================

class SubconDimensionalInline(admin.TabularInline):
    model = SubconJobworkDimensional
    extra = 1

class SubconVisualInline(admin.TabularInline):
    model = SubconJobworkvisulainspection
    extra = 1

class SubconReworkInline(admin.TabularInline):
    model = SubconJobworkreworkQty
    extra = 1

class SubconRejectInline(admin.TabularInline):
    model = SubconJobworkrejectQty
    extra = 1


@admin.register(SubconJobworkQCInfo)
class SubconJobworkQCInfoAdmin(admin.ModelAdmin):
    list_display = ('qc', 'qc_date', 'vendor', 'item', 'ok_qty')
    search_fields = ('qc', 'vendor', 'item')
    list_filter = ('qc_date',)
    inlines = [
        SubconDimensionalInline,
        SubconVisualInline,
        SubconReworkInline,
        SubconRejectInline
    ]


# =========================
# Sales Return QC
# =========================

class SalesReturnDimensionalInline(admin.TabularInline):
    model = SalesReturnDimensional
    extra = 1

class SalesReturnVisualInline(admin.TabularInline):
    model = SalesReturnvisulainspection
    extra = 1


@admin.register(SalesReturnQcInfo)
class SalesReturnQcInfoAdmin(admin.ModelAdmin):
    list_display = ('qc_no', 'qc_date', 'cust_vender_name', 'select_item', 'ok_qty')
    search_fields = ('qc_no', 'cust_vender_name', 'select_item')
    list_filter = ('qc_date',)
    inlines = [
        SalesReturnDimensionalInline,
        SalesReturnVisualInline
    ]


# =========================
# Register remaining models (optional direct view)
# =========================

admin.site.register(InwardtestDimensional)
admin.site.register(Inwardtestvisulainspection)
admin.site.register(InwardtestreworkQty)
admin.site.register(InwardtestrejectQty)

admin.site.register(SubconJobworkDimensional)
admin.site.register(SubconJobworkvisulainspection)
admin.site.register(SubconJobworkreworkQty)
admin.site.register(SubconJobworkrejectQty)

admin.site.register(SalesReturnDimensional)
admin.site.register(SalesReturnvisulainspection)