from django.db import models
from accounts.models import Department
# Create your models here.
# class VoucherModel(models.Model):
#     name = models.CharField(max_length=50)
    
class voucherDetail(models.Model):
    # user = models.ForeignKey(user)
    user_name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    voucher_code = models.IntegerField()
    details = models.CharField(max_length=500)
    amount = models.IntegerField()
    accounting_approval = models.BooleanField()
    mayor_approval = models.BooleanField()
    treasury_approval = models.BooleanField()
    date_time = models.DateTimeField(auto_now_add=True)

class DepartmentBugetDetails(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    added_budget = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)