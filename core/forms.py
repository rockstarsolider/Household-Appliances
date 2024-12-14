from django import forms  
from django.core.exceptions import ValidationError  
import re  


class PhoneNumberForm(forms.Form):  
    phone_number = forms.CharField(  
        max_length=15,  
        widget=forms.TextInput(attrs={  
            'placeholder': 'شماره تلفن',  
            'class': 'input input-bordered w-full mt-4',  
        }),  
        required=True  
    )  

    def clean_phone_number(self):  
        phone_number = self.cleaned_data.get('phone_number')  
        
        numeric_number = re.sub(r'\D', '', phone_number)  
        last_10_digits = numeric_number[-10:]   

        if len(last_10_digits) == 10:  
            normalized_number = '0' + last_10_digits  
            return normalized_number  
        else:  
            raise ValidationError('لطفا یک شماره تلفن معتبر وارد کنید.')

class RegisterForm(forms.Form):  
    otp = forms.CharField(  
        max_length=6,  
        widget=forms.TextInput(attrs={ 'placeholder': 'کد تایید', 'class': 'input input-bordered w-full mt-4'}),  
    )
    name = forms.CharField(  
        max_length=30,  
        widget=forms.TextInput(attrs={'placeholder': 'نام و نام خانوادگی',  'class': 'input input-bordered w-full mt-4',}),  
    )  

    def clean(self):
        name = self.cleaned_data.get('name')  
        otp = self.cleaned_data.get('otp')  

        if len(name) < 8:
            raise ValidationError('نام باید حداقل 8 کاراکتر باشد')
        
        if otp and not re.match(r'^\d+$', otp):  
            raise ValidationError('کد تایید باید فقط شامل اعداد باشد')  