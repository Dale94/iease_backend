from rest_framework.serializers import ModelSerializer
from .models import *

class Voucher_BudgetSerializer(ModelSerializer):
    class Meta:
        model = voucherDetail
        fields = '__all__'

class Voucher_AccountingSerializer(ModelSerializer):
    class Meta:
        model = voucherDetail
        fields = ['accounting_approval']

class Voucher_TreasurySerializer(ModelSerializer):
    class Meta:
        model = voucherDetail
        fields = ['treasury_approval']

class Voucher_MayorSerializer(ModelSerializer):
    class Meta:
        model = voucherDetail
        fields = ['mayor_approval']

class DepartmentBudgetSerializer(ModelSerializer):
    class Meta:
        model = DepartmentBugetDetails
        fields = '__all__'
