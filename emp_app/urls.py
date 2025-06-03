from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    
    # Admin URLs
    path('admin/dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin/add-employee/', views.AddEmployeeView.as_view(), name='add_employee'),
    path('admin/view-table/', views.EmployeeTableView.as_view(), name='view_table'),
    path('admin/delete-employee/<int:pk>/', views.DeleteEmployeeView.as_view(), name='delete_employee'),
    path('admin/leave-requests/', views.LeaveRequestListView.as_view(), name='leave_requests'),
    path('admin/approve-leave/<int:pk>/', views.ApproveLeaveView.as_view(), name='approve_leave'),
    path('admin/hr-requests/', views.HRRequestListView.as_view(), name='hr_requests'),
    path('admin/process-request/<int:pk>/', views.ProcessHRRequestView.as_view(), name='process_request'),
    
    # HR URLs
    path('hr/dashboard/', views.HRDashboardView.as_view(), name='hr_dashboard'),
    path('hr/view-table/', views.HREmployeeTableView.as_view(), name='hr_view_table'),
    path('hr/request-removal/<int:pk>/', views.RequestEmployeeRemovalView.as_view(), name='request_removal'),
    path('hr/submit-employee/', views.SubmitNewEmployeeView.as_view(), name='submit_employee'),
]