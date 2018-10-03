from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.views import View
from accounts import forms




class LoginView(generic.FormView):
	form_class = AuthenticationForm
	success_url = reverse_lazy("home")
	template_name = "accounts/login.html"

	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
		return form_class(self.request, **self.get_form_kwargs())

	# Takes users to success_url if the login...
	def form_valid(self, form):
		login(self.request, form.get_user())
		return super().form_valid(form)


class LogoutView(generic.RedirectView):
	url = reverse_lazy("home")

	def get(self, request, *args, **kwargs):
		logout(request)
		return super().get(request, *args, **kwargs)


# The default django signup form uses only username tp log users
# if you want to use email, then create form.py
class SignupView(generic.CreateView):
	form_class = forms.UserCreateForm
	success_url = reverse_lazy("login")
	template_name = "accounts/register.html"


class FollowersView(View):
	def get_object(self):
		object = super(FollowersView, self).get_object()
		object.follow_count += 1
		object.save()
		return object
