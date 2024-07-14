from django.urls import path, include
from .views import *



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    ############################# DEPARTMENT URLS ####################3
    path('list_department/', DepartmentListView.as_view()),
    path('<int:pk>/details_department/', GetDepartmentDetailsView.as_view()),
    path('create_department/', CreateDepartmentView.as_view()),
    path('<int:pk>/update_department/', UpdateDepartmentView.as_view()),
    path('<int:pk>/delete_department/', DeleteDepartentView.as_view()),

    ############################# DEPARTMENT URLS ####################3
    path('list_code/', EmployeeCodeListView.as_view()),
    path('<int:pk>/details_code/', GetEmployeeCodeDetailsView.as_view()),
    path('create__code/', CreateEmployeeCodeView.as_view()),
    path('<int:pk>/update__code/', UpdateEmployeeCodeView.as_view()),
    path('<int:pk>/delete__code/', DeleteEmployeeCodeView.as_view()),
    # path(r'^activate/(?P<uid>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z\-]+)/$', activate_account),
    
]