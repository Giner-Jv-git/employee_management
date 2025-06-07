from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import AddEmployeeView,EditEmployeeView,DeleteEmployeeView,EmployeeDetailView,HRDashboardView


urlpatterns = [
    #auth
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout_confirm'),
    
    #admin
    path('dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('add-employee/', AddEmployeeView.as_view(), name='add_employee'),
    path('employees/edit/<int:pk>/', EditEmployeeView.as_view(), name='edit_employee'),
    path('employees/delete/<int:pk>/', DeleteEmployeeView.as_view(), name='delete_employee'),
    path('employees/', views.EmployeeTableView.as_view(), name='view_table'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail'),

    #hr
    path('hr/hr_dashboard/', HRDashboardView.as_view(), name='hr_dashboard'),
]