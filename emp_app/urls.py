from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # View Table URLs
    path('employees/', views.EmployeeTableView.as_view(), name='view_table'),
    
    # If you need the HR view-only version
    

]