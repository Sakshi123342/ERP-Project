from django.db import models

# Create your models here.


class PendingBillGrnlist(models.Model):
    grn_no = models.CharField(max_length=200,blank=True,null=True)
    grn_date = models.DateField(blank=True,null=True)
    challan_no = models.CharField(max_length=200,blank=True,null=True)
    challan_date = models.DateField(blank=True,null=True)
    invoice_no = models.CharField(max_length=200,blank=True,null=True)
    invoice_date = models.DateField(blank=True,null=True)
    supplier_name = models.CharField(max_length=500,blank=True,null=True)
    po_no = models.CharField(max_length=200,blank=True,null=True)
    total = models.CharField(max_length=200,blank=True,null=True)
    user = models.CharField(max_length=200,blank=True,null=True)
    select = models.BooleanField(default=False,blank=True ,null=True)





class BillRegister(models.Model):
    plant = models.CharField(max_length=200, blank=True, null=True)
    bill_type = models.CharField(max_length=200, blank=True, null=True)
    series_no = models.CharField(max_length=200, blank=True, null=True)
    no = models.CharField(max_length=200, blank=True, null=True)
    supplier_name = models.CharField(max_length=500, blank=True, null=True)
    item_name = models.CharField(max_length=300, blank=True, null=True)
    rate = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    qty = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    fwd_charges = models.CharField(max_length=200, blank=True, null=True)
    transport_charged = models.CharField(max_length=200, blank=True, null=True)
    insurence = models.CharField(max_length=200, blank=True, null=True)
    installation_charges = models.CharField(max_length=200, blank=True, null=True)
    other_charges = models.CharField(max_length=200, blank=True, null=True)
    challan_date = models.DateField(blank=True, null=True)
    payment_days_terms = models.CharField(max_length=200, blank=True, null=True)
    tds = models.CharField(max_length=200, blank=True, null=True)
    sub_total = models.CharField(max_length=200, blank=True, null=True)
    challan_no = models.CharField(max_length=200, blank=True, null=True)
    payment_date = models.DateField(blank=True, null=True)
    other_amt = models.CharField(max_length=200, blank=True, null=True)
    assable_value = models.CharField(max_length=200, blank=True, null=True)
    posting_date = models.DateField(blank=True, null=True)
    round_of_amt = models.CharField(max_length=200, blank=True, null=True)
    net_total = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.no)


class BillRegisterItem(models.Model):
    bill_register = models.ForeignKey(BillRegister,on_delete=models.CASCADE,related_name='items',blank=True,null=True)
    grn_no = models.CharField(max_length=200, blank=True, null=True)
    chall_no = models.CharField(max_length=200, blank=True, null=True)
    po_no = models.CharField(max_length=200, blank=True, null=True)
    item_code = models.CharField(max_length=200, blank=True, null=True)
    item_no = models.CharField(max_length=200, blank=True, null=True)
    item_description = models.CharField(max_length=200, blank=True, null=True)
    hsn_code = models.CharField(max_length=200, blank=True, null=True)
    rate = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    grn_qty = models.CharField(max_length=200, blank=True, null=True)
    discount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    cgst = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    sgst = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    igst = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    cgst_amt = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    sgst_amt = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    igst_amt = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)

    glid = models.CharField(max_length=200, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.item_description)
    
class JobworkBillRegister(models.Model):
    series_no = models.CharField(max_length=200,blank=True,null=True)
    bill_no = models.CharField(max_length=200,blank=True,null=True)
    supplier = models.CharField(max_length=500,blank=True,null=True)
    inv_challan_no= models.CharField(max_length=200,blank=True,null=True)
    inv_challan_date = models.DateField(blank=True,null=True)
    payment_terms_days = models.CharField(max_length=200,blank=True,null=True)
    payment_date = models.DateField(blank=True,null=True)
    posting_date = models.DateField(blank=True,null=True)
    sub_total = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    assable_value = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    tds = models.CharField(max_length=200,blank=True,null=True)
    tcs = models.CharField(max_length=200,blank=True,null=True)
    round_of_amt = models.CharField(max_length=200,blank=True,null=True)
    grand_total=  models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    pack_forward_charge = models.CharField(max_length=200,blank=True,null=True)
    transport_charge = models.CharField(max_length=200,blank=True,null=True)
    insurance = models.CharField(max_length=200,blank=True,null=True)
    installation_charge = models.CharField(max_length=200,blank=True,null=True)
    other_charge = models.CharField(max_length=200,blank=True,null=True)
    ohter_amount = models.CharField(max_length=200,blank=True,null=True)
    add_item = models.CharField(max_length=200,blank=True,null=True)
    total_qty = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    sub_total = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    dis_total = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    basic_total = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    cgst_total = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    sgst_total = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    igst_total = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    total_tax= models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    other_charge = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    bill_amount = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    tds_amt = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    tcs_amt = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    final_amount = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    remark = models.TextField(blank=True,null=True)

    def __str__(self):
        return str(self.bill_no)


class JobworkBillRegisterItem(models.Model):
    bill_register = models.ForeignKey(JobworkBillRegister,on_delete=models.CASCADE,related_name='items',blank=True,null=True)
    grn_no = models.CharField(max_length=200,blank=True,null=True)
    chal_no = models.CharField(max_length=200,blank=True,null=True)
    po_no = models.CharField(max_length=200,blank=True,null=True)
    item_no = models.CharField(max_length=200,blank=True,null=True)
    item_code = models.CharField(max_length=200,blank=True,null=True)
    item_description = models.CharField(max_length=200,blank=True,null=True)
    hsn_code = models.CharField(max_length=200,blank=True,null= True)
    rate = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    grn_qty = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    challan_qty = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    dis = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    dis_amt = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    total = models.DecimalField(max_digits=50,decimal_places=2,blank=True,null=True)
    cgst = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    sgst = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    igst = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    cgst_amt = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    sgst_amt = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    igst_amt = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    glid = models.CharField(max_length=200,blank=True,null=True)
    tds = models.BooleanField(blank=True,null=True,default=False)

    def __str__(self):
        return str(self.item_no)


class GeneralLedgerMaster(models.Model):
    gl_code  = models.CharField(max_length=200,blank=True,null=True)
    gl_description = models.CharField(max_length=500,blank=True , null=True)
    gl_category = models.CharField(max_length=200,blank=True,null=True)
    user = models.CharField(max_length=200,blank=True,null=True)
    



