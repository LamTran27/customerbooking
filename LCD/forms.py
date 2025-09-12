from django import forms
from .models import Customer
from .models import Pictures

# class CustomerForm(forms.ModelForm):
#     class Meta:
#         model = Customer
#         fields = '__all__'
#         widgets = {
#             'note': forms.TextInput(attrs={'size': 50}),  # 👈 đặt ở đây
#         }

class PicturesForm(forms.ModelForm):
    class Meta:
        model = Pictures
        fields = '__all__'
        widgets = {
            'AddDate': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'DeletedDate': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'plate', 'note', 'adddate', 'KHDV', 'CVDV']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên khách hàng'}),
            'plate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Biển số xe'}),
            'note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ghi chú'}),
            'adddate': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }, format='%Y-%m-%dT%H:%M'),
            'KHDV': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Khoang DV'}),
            'CVDV': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cố vấn DV'}),
        }

class PictureForm(forms.ModelForm):
    class Meta:
        model = Pictures
        fields = ['pictureName']
        widgets = {
            'pictureName': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }

