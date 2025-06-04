
from django import forms
from .models import EmployeeData

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = EmployeeData
        fields = ['name', 'profile_picture', 'employee_id', 'phone_number', 
                 'age', 'salary', 'address', 'status']
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'placeholder': '09XXXXXXXXX',
                'pattern': '09\d{9}',
                'title': '11 digits starting with 09'
            }),
            'age': forms.NumberInput(attrs={'min': 18}),
            'salary': forms.NumberInput(attrs={'step': '0.01'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }