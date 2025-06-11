from django import forms
from .models import EmployeeData

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = EmployeeData
        fields = ['name', 'profile_picture', 'employee_id', 'phone_number', 
                 'age', 'salary', 'address', 'status', 'position']
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'placeholder': '09XXXXXXXXX',
                'pattern': '09\d{9}',
                'title': '11 digits starting with 09'
            }),
            'age': forms.NumberInput(attrs={'min': 18}),
            'salary': forms.NumberInput(attrs={'step': '0.01'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'profile_picture': forms.FileInput(attrs={
                'accept': 'image/*',
                'class': 'hidden'
            })
        }

class HRAddEmployeeRequestForm(forms.Form):
    name = forms.CharField(max_length=100)
    employee_id = forms.CharField(max_length=20)
    age = forms.IntegerField(min_value=18)
    salary = forms.DecimalField(max_digits=10, decimal_places=2)
    address = forms.CharField(widget=forms.Textarea)
    phone_number = forms.CharField(max_length=11)
    position = forms.ChoiceField(choices=EmployeeData.POSITION_CHOICES)
    # Add other fields as needed