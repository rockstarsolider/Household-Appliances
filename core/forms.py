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
        
class EmailForm(forms.Form):  
    email = forms.CharField(  
        max_length=100,  
        widget=forms.TextInput(attrs={  
            'placeholder': 'ایمیل',  
            'class': 'input input-bordered w-full mt-4',  
        }),  
        required=True  
    )  
    password = forms.CharField(  
        widget=forms.PasswordInput(attrs={  
            'placeholder': 'رمز عبور',  
            'class': 'input input-bordered w-full mt-4',  
        }),  
        required=True,  
          # Minimum length for password  
    )  

    def clean_email(self):  
        email = self.cleaned_data.get('email')  
        if email:  
            # Basic validation to check if the input is a valid email format  
            if not self.is_valid_email(email):  
                raise ValidationError("فرمت ایمیل نامعتبر است.")  
        return email  

    def clean_password(self):  
        password = self.cleaned_data.get('password')  
        if password:  
            # Custom validation for the password  
            if not self.is_valid_password(password):  
                raise ValidationError("رمز عبور باید حداقل 8 کاراکتر شامل حروف بزرگ و کوچک و اعداد باشد.")  
        return password  

    def is_valid_email(self, email):  
        # Regex pattern for basic email validation  
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'  
        return re.match(pattern, email) is not None  

    def is_valid_password(self, password):  
        # Check if password has at least one lowercase, one uppercase, and one number  
        return (len(password) >= 8 and  
                re.search(r'[A-Z]', password) and  
                re.search(r'[a-z]', password) and  
                re.search(r'[0-9]', password))  

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