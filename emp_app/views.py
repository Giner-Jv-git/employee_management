from django.views.generic import ListView,TemplateView,CreateView,UpdateView,DeleteView,DetailView,FormView, View
from django.db.models import Q
from .models import EmployeeData, HRRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import EmployeeForm, HRAddEmployeeRequestForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from decimal import Decimal






#auth

def login_view(request):
    if request.user.is_authenticated:
        # Redirect based on role
        if hasattr(request.user, 'employeeprofile'):
            if request.user.employeeprofile.role == 'admin':
                return redirect('admin_dashboard')
            elif request.user.employeeprofile.role == 'hr':
                return redirect('hr_dashboard')
        return redirect('admin_dashboard')  # fallback

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect based on role
            if hasattr(user, 'employeeprofile'):
                if user.employeeprofile.role == 'admin':
                    return redirect('admin_dashboard')
                elif user.employeeprofile.role == 'hr':
                    return redirect('hr_dashboard')
            return redirect('admin_dashboard')  # fallback
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'emp_app/login.html')

def logout_confirm_view(request):
    return render(request, 'emp_app/logout_confirm.html')

def logout_view(request):

    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('logout_confirm')


#admin
#dashboard functions

class AdminDashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'emp_app/admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_employees'] = EmployeeData.objects.count()
        context['active_employees'] = EmployeeData.objects.filter(status='active').count()
        context['inactive_employees'] = EmployeeData.objects.filter(status='inactive').count()
        
        # Recent updates (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        context['recent_updates'] = EmployeeData.objects.filter(
            updated_at__gte=thirty_days_ago
        ).count()
        
        # Recently modified employees (last 5 changes)
        context['recent_employees'] = EmployeeData.objects.all().order_by('-updated_at')[:5]
        
        # Pie chart data
        position_labels = [label for _, label in EmployeeData.POSITION_CHOICES]
        position_counts = [
            EmployeeData.objects.filter(position=key).count()
            for key, _ in EmployeeData.POSITION_CHOICES
        ]
        context['position_labels'] = position_labels
        context['position_counts'] = position_counts
        return context


#add employee

class AddEmployeeView(LoginRequiredMixin, CreateView):
    model = EmployeeData
    form_class = EmployeeForm
    template_name = 'emp_app/admin/add_employee.html'
    success_url = reverse_lazy('view_table')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Employee added successfully!')
        return response


#employee view 

class EmployeeTableView(LoginRequiredMixin,ListView):
    model = EmployeeData
    template_name = 'emp_app/admin/view_table.html'
    context_object_name = 'employees'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        status_filter = self.request.GET.get('status', '')

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(employee_id__icontains=search_query) |
                Q(phone_number__icontains=search_query) |
                Q(address__icontains=search_query)
            )

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['status_filter'] = self.request.GET.get('status', '')
        return context

#edit employee

class EditEmployeeView(LoginRequiredMixin, UpdateView):
    model = EmployeeData
    form_class = EmployeeForm
    template_name = 'emp_app/admin/edit_employee.html'
    success_url = reverse_lazy('view_table')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee'] = self.get_object()  # Pass employee object to template
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Employee updated successfully!')
        return response

#delete Emp

class DeleteEmployeeView(LoginRequiredMixin, DeleteView):
    model = EmployeeData
    success_url = reverse_lazy('view_table')
    template_name = 'emp_app/admin/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee'] = self.get_object()
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Employee deleted successfully!')
        return response

#employee detail view

class AdminEmployeeDetailView(LoginRequiredMixin, DetailView):
    model = EmployeeData
    template_name = 'emp_app/admin/employee_detail.html'
    context_object_name = 'employee'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee'] = self.get_object()
        return context

class HREmployeeDetailView(LoginRequiredMixin, DetailView):
    model = EmployeeData
    template_name = 'emp_app/hr/hr_employee_detail.html'
    context_object_name = 'employee'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee'] = self.get_object()
        return context

#hr
#hr dashboard
def is_hr(user):
    return hasattr(user, 'employeeprofile') and user.employeeprofile.role == 'hr'

@method_decorator([login_required, user_passes_test(is_hr)], name='dispatch')
class HRDashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'emp_app/hr/hr_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_employees'] = EmployeeData.objects.count()
        context['active_employees'] = EmployeeData.objects.filter(status='active').count()
        context['inactive_employees'] = EmployeeData.objects.filter(status='inactive').count()
        
        # Recent updates (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        context['recent_updates'] = EmployeeData.objects.filter(
            updated_at__gte=thirty_days_ago
        ).count()
        
        # Recently modified employees (last 5 changes)
        context['recent_employees'] = EmployeeData.objects.all().order_by('-updated_at')[:5]
        
        # Pie chart data
        position_labels = [label for _, label in EmployeeData.POSITION_CHOICES]
        position_counts = [
            EmployeeData.objects.filter(position=key).count()
            for key, _ in EmployeeData.POSITION_CHOICES
        ]
        context['position_labels'] = position_labels
        context['position_counts'] = position_counts
        return context

     

class HREmployeeTableView(ListView):
    model = EmployeeData
    template_name = 'emp_app/hr/hr_view_table.html'  # Create this template
    context_object_name = 'employees'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        status_filter = self.request.GET.get('status', '')

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(employee_id__icontains=search_query) |
                Q(phone_number__icontains=search_query) |
                Q(address__icontains=search_query)
            )

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['status_filter'] = self.request.GET.get('status', '')
        return context

# HR Add Employee Request

class HRAddEmployeeRequestView(FormView):
    template_name = 'emp_app/hr/hr_add_employee_request.html'
    form_class = HRAddEmployeeRequestForm
    success_url = reverse_lazy('hr_request_list')

    def form_valid(self, form):
        data = form.cleaned_data.copy()
        # Convert all Decimal values to float for JSON serialization
        for key, value in data.items():
            if isinstance(value, Decimal):
                data[key] = float(value)
        HRRequest.objects.create(
            request_type='add_employee',
            employee_data=data,
            request_by=self.request.user
        )
        return super().form_valid(form)

class HRRequestListView(ListView):
    model = HRRequest
    template_name = 'emp_app/hr/hr_request_list.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return HRRequest.objects.filter(request_by=self.request.user).order_by('-created_at')

class AdminHRRequestListView(ListView):
    model = HRRequest
    template_name = 'emp_app/admin/hr_request_admin_list.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return HRRequest.objects.filter(status='pending').order_by('-created_at')

class AdminHRRequestProcessView(View):
    def post(self, request, pk):
        hr_request = get_object_or_404(HRRequest, pk=pk)
        action = request.POST.get('action')
        if action == 'approve':
            hr_request.status = 'approved'
            hr_request.processed_by = request.user
            hr_request.updated_at = timezone.now()
            # If it's an add_employee request, create the EmployeeData
            if hr_request.request_type == 'add_employee' and hr_request.employee_data:
                EmployeeData.objects.create(
                    **hr_request.employee_data,
                    created_by=hr_request.request_by
                )
        elif action == 'reject':
            hr_request.status = 'rejected'
            hr_request.processed_by = request.user
            hr_request.updated_at = timezone.now()
        hr_request.save()
        return redirect('admin_hr_requests')



class HRRequestDeleteView(DeleteView):
    model = HRRequest
    template_name = 'emp_app/hr/hr_request_confirm_delete.html'
    success_url = reverse_lazy('hr_request_list')

    def get_queryset(self):
        # Only allow the user to delete their own requests
        return HRRequest.objects.filter(request_by=self.request.user)