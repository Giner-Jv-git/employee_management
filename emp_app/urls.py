from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    #auth
    path('login/', views.login_view, name='login'),
    #admin
    path('dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    # View Table URLs
    path('employees/', views.EmployeeTableView.as_view(), name='view_table'),
    
    # If you need the HR view-only version
    

]