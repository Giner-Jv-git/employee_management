from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import AddEmployeeView,EditEmployeeView,DeleteEmployeeView,AdminEmployeeDetailView,HRDashboardView,HREmployeeTableView,HREmployeeDetailView


urlpatterns = [
    #auth
    path('login/', views.login_view, name='login'),
    path('logout/confirm/', views.logout_confirm_view, name='logout_confirm'), 
    path('logout/', views.logout_view, name='logout'), # confirmation page
    
    #admin
    path('dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('add-employee/', AddEmployeeView.as_view(), name='add_employee'),
    path('employees/edit/<int:pk>/', EditEmployeeView.as_view(), name='edit_employee'),
    path('employees/delete/<int:pk>/', DeleteEmployeeView.as_view(), name='delete_employee'),
    path('employees/', views.EmployeeTableView.as_view(), name='view_table'),
    path('employees/<int:pk>/',AdminEmployeeDetailView.as_view(), name='admin_employee_detail'),

    #hr
    path('hr/hr_dashboard/', HRDashboardView.as_view(), name='hr_dashboard'),
    path('hr/employees/', HREmployeeTableView.as_view(), name='hr_view_table'),
    path('hr/employees/<int:pk>/', HREmployeeDetailView.as_view(), name='hr_employee_detail'),
]