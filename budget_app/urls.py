from django.urls import path, include
# from rest_framework import routers
from .views import *

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # path('', include(router.urls)),
    path('', GetVoucherListView),
    path('<int:pk>/detail_voucher/', GetVoucherDetailsView),
    path('<int:pk>/create_voucher/', CreateVoucherView),
    path('<int:pk>/approve_accounting/', AprroveAccoutingView),
    path('<int:pk>/approve_mayor/', AprroveMayorView),
    path('<int:pk>/approve_treasury/', AprroveTreasuryView),
    path('<int:pk>/create_budget/', CreateBudgetView),
    path('DepartmentBudget/', GetDepartmentBudgetListView),



]