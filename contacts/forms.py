from django import forms

class contactForm(forms.Form):
    name = forms.CharField(required = True, max_length = 100, label='')
    email = forms.EmailField(required = True, max_length = 100, label='')
    phone = forms.RegexField(regex=r'^\+?1?\d{11,13}$', label='')
    comment = forms.CharField(widget=forms.Textarea,label='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'your name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'your email eg. email@example.com'})
        self.fields['phone'].widget.attrs.update({'placeholder': 'your mobile eg. +234-8123456789'})
        self.fields['comment'].widget.attrs.update({'rows': '3', 'placeholder': 'your message here...'})
