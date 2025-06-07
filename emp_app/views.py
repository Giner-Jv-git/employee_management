from django.views.generic import ListView,TemplateView,CreateView,UpdateView,DeleteView,DetailView
from django.db.models import Q
from .models import EmployeeData
from django.shortcuts import render, redirect
from django.contrib import messages

from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import EmployeeForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator



#auth

def login_view(request):
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

def logout_confirm(request):
    return render(request, 'emp_app/logout_confirm.html')

#admin
#dashboard functions

class AdminDashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'emp_app/admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Total employees count
        context['total_employees'] = EmployeeData.objects.count()
        
        # Active employees count
        context['active_employees'] = EmployeeData.objects.filter(status='active').count()
        
        # Recent updates (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        context['recent_updates'] = EmployeeData.objects.filter(
            updated_at__gte=thirty_days_ago
        ).count()
        
        # Recently modified employees (last 5 changes)
        context['recent_employees'] = EmployeeData.objects.all().order_by('-updated_at')[:5]
        
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

class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = EmployeeData
    template_name = 'emp_app/admin/employee_detail.html'
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
        
        # Total employees count
        context['total_employees'] = EmployeeData.objects.count()
        
        # Active employees count
        context['active_employees'] = EmployeeData.objects.filter(status='active').count()
        
        # Recent updates (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        context['recent_updates'] = EmployeeData.objects.filter(
            updated_at__gte=thirty_days_ago
        ).count()
        
        # Recently modified employees (last 5 changes)
        context['recent_employees'] = EmployeeData.objects.all().order_by('-updated_at')[:5]
        
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
    
#hr employee detail view

class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = EmployeeData
    template_name = 'emp_app/hr/hr_employee_detail.html'
    context_object_name = 'employee'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee'] = self.get_object()
        return context