from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from crispy_forms.layout import (Layout, Row, Column)
from crispy_forms.helper import FormHelper
# from crispy_forms_gds.helper import FormHelper
# from crispy_forms_gds.layout import Field, Layout, Size, Submit



class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField()
	last_name = forms.CharField()
	class Meta:
		model = User
		fields = ("username", "email", "first_name","last_name", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user