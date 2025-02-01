from django import forms  

class OrderForm(forms.Form):  
    name = forms.CharField(  
        label='نام و نام خانوادگی:',  
        widget=forms.TextInput(attrs={'class': 'input input-bordered w-full mb-4 mt-1'}),  
    )  
    postal_code = forms.CharField(  
        label='کد پستی:',  
        widget=forms.TextInput(attrs={'class': 'input input-bordered w-full mb-4 mt-1'}),  
    )  
    shipping_address = forms.CharField(  
        label='آدرس:',  
        widget=forms.Textarea(attrs={'class': 'textarea input-bordered w-full mb-4 mt-1', 'rows': 3}),  
    )  

    def clean_name(self):  
        name = self.cleaned_data.get('name')  
        if not name:  
            raise forms.ValidationError("نام و نام خانوادگی الزامی است.")  
        return name    
    
    def clean_postal_code(self):  
        postal_code = self.cleaned_data.get('postal_code')  
        if not postal_code:  
            raise forms.ValidationError("کد پستی الزامی است")
        if len(postal_code) != 10:
            raise forms.ValidationError("طول کد پستی باید 10 رقم باشد")  
        return postal_code    

    def clean_shipping_address(self):  
        shipping_address = self.cleaned_data.get('shipping_address')  
        if not shipping_address:  
            raise forms.ValidationError("آدرس حمل و نقل الزامی است.")  
        return shipping_address   