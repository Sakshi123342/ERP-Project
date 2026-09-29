from django.db import models

# Create your models here.


class ToolManagement(models.Model):
    item_no = models.CharField(max_length=500,blank=True,null=True)
    item_description = models.CharField(max_length=500,blank=True,null=True)
    part_code = models.CharField(max_length=200,blank=True,null=True)
    tool_code = models.CharField(max_length=500,blank=True,null=True)
    tool_description = models.CharField(max_length=500,blank=True,null=True)
    make = models.CharField(max_length=200,blank=True,null=True)
    tool_life= models.CharField(max_length=200,blank=True,null=True)
    no_of_reshaping_tool = models.CharField(max_length=500,blank=True,null=True)
    total_life = models.CharField(max_length=200,blank=True,null=True)
    total_required = models.DecimalField(max_digits=50,decimal_places=5,blank=True,null=True)

    