from django import forms  
from django.contrib.auth.forms import PasswordChangeForm  
from core.models import CustomUser  
from django.core.exceptions import ValidationError  

class CustomUserUpdateForm(forms.ModelForm):  
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={ 
            'label':'ایمیل:', 
            'placeholder': 'ایمیل',  
            'class': 'input input-bordered w-full mb-4 mt-1',  
        }), 
    )  
    
    class Meta:  
        model = CustomUser  
        fields = ['email'] 
        
    def clean_email(self):  
        email = self.cleaned_data.get('email')  
        
        # Ensure the email is unique  
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():  
            raise ValidationError("This email is already in use.")  
        return email   

class CustomPasswordForm(forms.Form):  
    password1 = forms.CharField(  
        label='رمز جدید:',  
        widget=forms.PasswordInput(attrs={'class': 'input input-bordered w-full mb-4 mt-1'}),  
        min_length=8,  # Set a minimum length if needed  
    )  
    password2 = forms.CharField(  
        label='تکرار رمز جدید:',  
        widget=forms.PasswordInput(attrs={'class': 'input input-bordered w-full mb-4 mt-1'}),  
    )  

    def clean(self):  
        cleaned_data = super().clean()  
        password1 = cleaned_data.get("password1")  
        password2 = cleaned_data.get("password2")  

        # Check if the two password fields match  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("رمز عبور جدید و تکرار آن مطابقت ندارد.")  

        # You can add more validations here as needed  
        return cleaned_data