from email.policy import default
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.

class NewUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    address = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ("first_name","last_name","username", "email", "password1", "password2", "address")
        model._meta.get_field('email')._unique = True

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.username = user.username.lower()
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.address = self.cleaned_data['address']
        if commit:
            user.save()
        return user




# from dataclasses import fields
# from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from django import forms


# class CreateUserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']
#         # widgets = {
#         #     'username': TextInput(attrs={
#         #         'class': "u-border-3 u-border-no-left u-border-no-right u-border-no-top u-border-white u-input u-input-rectangle u-input-2",
#         #         'placeholder': 'Enter your Username'
#         #     }),
#         #     'email': EmailInput(attrs={
#         #         'class': "u-border-3 u-border-no-left u-border-no-right u-border-no-top u-border-white u-input u-input-rectangle u-input-1",
#         #         'placeholder': 'Enter a valid Email'
#         #     }),
#         #     'password': PasswordInput(attrs={
#         #         'class': "u-border-3 u-border-no-left u-border-no-right u-border-no-top u-border-white u-input u-input-rectangle u-input-2",
#         #         'placeholder': 'Enter Password'
#         #     })
#         # }
