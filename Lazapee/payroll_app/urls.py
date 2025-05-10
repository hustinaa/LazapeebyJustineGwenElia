from django.contrib import admin
from django.urls import path
from .import views
app_name = 'payroll_app'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.employee_page, name='employee_page'),
    path('employee_page/', views.employee_page, name='employee_page'),
    path('create_employee/', views.create_employee, name='create_employee'),
    path('payslips_page/',views.payslips_page, name='payslips_page'),
    path('add_overtime/<int:employee_id>/', views.add_overtime, name='add_overtime'),
    path('delete_employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('update_employee/<int:employee_id>/', views.update_employee, name='update_employee'),
    path('update_employee/update_record/<int:employee_id>/', views.update_record, name="update_record"),
    path('search_employee', views.search_employee, name='search_employee'),
    path('view_payslips/<str:id_number>/<int:year>/<str:month>/<int:cycle>/', views.view_payslips, name='view_payslips'),
]
