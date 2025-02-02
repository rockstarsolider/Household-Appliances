from django import forms  
from django.core.exceptions import ValidationError  

class CommentForm(forms.Form):  
    text = forms.CharField(
        max_length=300,
        widget=forms.Textarea(attrs={ 'placeholder': 'دیدگاه خود را وارد کنید...', 'class': 'textarea input-bordered w-full ', 'rows':'4'}),  
    ) 

    def clean_text(self):
        text = self.cleaned_data.get('text')  

        if len(text) < 10:
            raise ValidationError('متن باید حداقل 10 حرف باشد')
        if len(text) > 299:
            raise ValidationError('متن باید حداکثر 300 حرف باشد')
        return text