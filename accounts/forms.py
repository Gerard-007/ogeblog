from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.widgets import PasswordInput, TextInput

class CustomAuthForm(AuthenticationForm):
	username = forms.CharField(widget=TextInput(attrs={'placeholder': 'email@example.com'}), label='')
	password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'password'}), label='')

class UserCreateForm(UserCreationForm):
	class Meta:
		fields = ("username", "email", "password1", "password2")
		model = get_user_model()


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["username"].widget.attrs.update({'placeholder': 'fullname'})
		self.fields["email"].widget.attrs.update({'placeholder': 'example@email.com'})
		self.fields["password1"].widget.attrs.update({'placeholder': 'password'})
		self.fields["password2"].widget.attrs.update({'placeholder': 'confirm password'})
		self.fields["username"].label = ""
		self.fields["email"].label = ""
		self.fields["password1"].label = ""
		self.fields["password2"].label = ""
		self.fields["password1"].help_text = "<span class='text-muted' style='font-size:10px'>Your password must be 8 character & above mixed with leters & numbers</span>"
		self.fields["password2"].help_text = "<span class='text-muted' style='font-size:10px'>Repeat the password again</span>"
