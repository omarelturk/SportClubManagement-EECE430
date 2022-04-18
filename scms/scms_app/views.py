#from multiprocessing import context
from multiprocessing import context
from os import stat
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from requests import request
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
import netifaces as ni
from scms_app.models import Football_Player, Basketball_Player, Ticket


from .models import *
from .forms import NewUserForm

ip = ni.ifaddresses('en0')[ni.AF_INET][0]['addr']


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            #login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("Signin.html")
        messages.error(request, "Unsuccessful registration. Invalid information.")
        print(form.errors)
        form_errors = form.errors
        return render(request=request, template_name="Signup.html", context={"register_form": form, "form_errors":form_errors})

    form = NewUserForm()
    return render(request=request, template_name="Signup.html", context={"register_form": form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request,"Invalid username or password.")
                form_errors = form.errors
                return render(request=request, template_name="Signin.html", context={"login_form":form, "form_errors":form_errors})
        else:
            messages.error(request,"Invalid username or password.")
            form_errors = form.errors
            return render(request=request, template_name="Signin.html", context={"login_form":form, "form_errors":form_errors})
    form = AuthenticationForm()
    return render(request=request, template_name="Signin.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("Home")

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':f'{ip}:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:

						return HttpResponse('Invalid header found.')
						
					messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
					return redirect ("/")
			messages.error(request, 'An invalid email has been entered.')
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})




###############################################################################################

def Home(request):
    return render(request, 'Home.html', {})


def About(request):
    return render(request, 'About.html', {})


def StadiumMuseum(request):
    return render(request, 'StadiumMuseum.html', {})


def TeamsB(request):
    context={}
    if request.method == 'GET':
        bplayers = Basketball_Player.objects.all()
        context['players'] = bplayers
        return render(request, 'TeamsB.html', context)


def TeamsF(request):
    context={}
    if request.method == 'GET':
        fplayers = Football_Player.objects.all()
        context['players'] = fplayers
        return render(request, 'TeamsF.html', context)
            
            # else:
            #     messages.error(request, 'Player sport type was not chosen.') 
        

def Fixtures(request):
    return render(request, 'Fixtures.html', {})

def Tickets(request):
    context={}
    if request.method == 'GET':
        tickets = Ticket.objects.all()
        context["tickets"] = tickets
        return render(request, 'Tickets.html', context)

def Shop(request):
    return render(request, 'Shop.html', {})

def News(request):
    return render(request, 'News.html', {})    