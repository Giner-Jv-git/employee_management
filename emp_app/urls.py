from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import AddEmployeeView

urlpatterns = [
    #auth
    path('login/', views.login_view, name='login'),
    #admin
    path('dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('add-employee/', AddEmployeeView.as_view(), name='add_employee'),
    path('employees/', views.EmployeeTableView.as_view(), name='view_table'),
    
    # If you need the HR view-only version
    

]