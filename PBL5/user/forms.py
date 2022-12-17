from operator import xor
from django import forms
from .models import *

class StudentForm(forms.ModelForm):
    code = forms.CharField(
        label='Code: ',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter code here'
            }
        )
    )
    fullname = forms.CharField(
        label='Fullname: ',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter fullname here'
            }
        )
    )
    avatar = forms.ImageField(
        label='Avatar: ',
        required=False,
        allow_empty_file=True,
    )
    
    class Meta:
        model = Student
        fields = [
            'code',
            'fullname',
            'avatar'
            ]

# create code for clean_code without having characters and not same code
    def clean_code(self):
        code = self.cleaned_data.get('code')
        if code.isdigit() == False:
            raise forms.ValidationError("Code must be number")
        if Student.objects.filter(code=code).exists() and self.instance == None:
            raise forms.ValidationError("Code already exists")
        if len(code) != 9:
            raise forms.ValidationError("Code must be 9 characters")
        return code

    #create code for clean_fullname without including numbers
    def clean_fullname(self):
        fullname = self.cleaned_data.get('fullname')
        if fullname.isdigit() == True:
            raise forms.ValidationError("Fullname must be characters")
        return fullname