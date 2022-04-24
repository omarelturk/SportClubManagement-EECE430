#from multiprocessing import context
from multiprocessing import context
from os import stat
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from requests import request, session
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
from scms_app.models import Football_Player, Basketball_Player, Football_Ticket, Basketball_Ticket, Profile
from sys import platform
from django.core.files.storage import FileSystemStorage


from .models import *
from .forms import NewUserForm


if platform == "linux" or platform == "linux2":
	# linux
	ip = ni.ifaddresses('en0')[ni.AF_INET][0]['addr']
elif platform == "darwin":
	# OS X
	ip = ni.ifaddresses('en0')[ni.AF_INET][0]['addr']
elif platform == "win32":
	# Windows
	ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST, request.FILES)
		user_select = request.POST["users_type"]
		if user_select == "normaluser":
			if form.is_valid():
				formusername = form.cleaned_data.get('username')
				formaddress = form.cleaned_data.get('address')
				form.save()

				print("LOOOK HHEREEEEEE")
				print(request.FILES)

				userImageExist = request.FILES.get('userImage', False)
				if userImageExist is True:
					userImage = request.FILES['userImage']
					fss = FileSystemStorage()
					file = fss.save(userImage.name, userImage)
					file_url = fss.url(file)
				else:
					file_url = None

				user = User.objects.get(username=formusername)

				if file_url is None:
					profile = Profile(username_id=user.id, address=formaddress, balance=0)
					profile.save()
				else:
					profile = Profile(username_id=user.id, userimage=file_url, address=formaddress, balance=0)
					profile.save()

				messages.success(request, "Registration successful.")
				return redirect("Signin.html")
		else:
			if form.is_valid():
				form.save()
				user = User.objects.get(username=form.cleaned_data.get('username'))
				user.is_staff = True
				user.save()
				messages.success(request, "Registration as staff successful.")
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
		if User.objects.filter(username=request.POST["username"]).exists():
			user = User.objects.get(username=request.POST["username"])
		else:
			print("MESSAGE SHOULD SHOW")
			messages.warning(request, "User Does Not Exist!")
			return redirect("Signin.html")
		print(user.is_staff)
		if user.is_staff is False:
			if form.is_valid():
				username = form.cleaned_data.get('username')
				password = form.cleaned_data.get('password')
				user = authenticate(username=username, password=password)
				request.session["normaluser"] = username
				# print(request.session["normaluser"])
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

		elif user.is_staff is True:
			if form.is_valid():
				username = form.cleaned_data.get('username')
				password = form.cleaned_data.get('password')
				user = authenticate(username=username, password=password)
				request.session["staffuser"] = username
				# print(request.session["normaluser"])
				if user is not None:
					login(request, user)
					messages.info(request, f"You are now logged in as staff member {username}.")
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
	#logout(request)
	request.session.flush()
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
	profiles = Profile.objects.all()
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form, "profiles": profiles})

def addBalance(request):
	if request.method == "POST":
		session_user_id = request.session.get('_auth_user_id')
		amount_added = request.POST["amount_added"]
		context={}
		profiles = Profile.objects.all()
		context['profiles'] = profiles
		for profile in profiles:
			if int(profile.username_id) == int(session_user_id):
				old_balance = int(profile.balance)
				print(old_balance)
				new_balance = old_balance+int(amount_added)
				profile.balance = new_balance
				profile.save()

# BASKETBALL PLAYERS

def addBasketballPlayer(request):
	context={}
	if request.method == "POST" and request.FILES['playerImage']:
		playerName = request.POST['playerName']
		playerNumber = request.POST['playerNumber']
		playerPosition = request.POST['playerPosition']
		playerNationality = request.POST['playerNationality']
		
		playerImage = request.FILES['playerImage']
		fss = FileSystemStorage()
		file = fss.save(playerImage.name, playerImage)
		file_url = fss.url(file)

		print(file_url)

		bplayer = Basketball_Player(
			player_name=playerName, 
			player_number=playerNumber, 
			player_position=playerPosition, 
			player_nationality=playerNationality, 
			player_image=file_url
		)
		bplayer.save()
	bplayers = Basketball_Player.objects.all()
	context['players'] = bplayers
	return redirect("TeamsB.html", context=context)

def removeBasketballPlayer(request):
	context={}
	arr = []
	if request.method == "POST":
		for key in request.POST.keys():
			arr.append(key)
		removeBtn = arr[1]
		print(removeBtn)
		bplayerdelete = Basketball_Player.objects.get(id=removeBtn)
		bplayerdelete.delete()
	bplayers = Basketball_Player.objects.all()
	context['players'] = bplayers
	return redirect("TeamsB.html", context=context)

def updateBasketballPlayer(request):
	context={}
	arr = []
	if request.method == "POST":
		
		playerId = request.POST["updateBtn"]
		playerName = request.POST['playerName']
		playerNumber = request.POST['playerNumber']
		playerPosition = request.POST['playerPosition']
		playerNationality = request.POST['playerNationality']
		print([playerId, playerName, playerNumber, playerPosition, playerNationality])


		print("BREAK")
		print(request.FILES['playerImage'])
		# if request.FILES['playerImage'] != None:
		# 	playerImage = request.FILES['playerImage']
		# 	fss = FileSystemStorage()
		# 	file = fss.save(playerImage.name, playerImage)
		# 	file_url = fss.url(file)

		# 	bplayerupdate = Basketball_Player(
		# 		id=playerId, 
		# 		player_name=playerName, 
		# 		player_number=playerNumber, 
		# 		player_position=playerPosition, 
		# 		player_nationality=playerNationality, 
		# 		player_image=file_url
		# 		)

		# 	bplayerupdate.save()
			
		# else:
		bplayerupdate = Basketball_Player.objects.filter(id=playerId)
		
		bplayerupdate.update(
			player_name=playerName, 
			player_number=playerNumber, 
			player_position=playerPosition, 
			player_nationality=playerNationality, 
		)

	bplayers = Basketball_Player.objects.all()
	context['players'] = bplayers
	return redirect("TeamsB.html", context=context)

# FOOTBALL PLAYERS

def addFootballPlayer(request):
	context={}
	if request.method == "POST" and request.FILES['playerImage']:
		playerName = request.POST['playerName']
		playerNumber = request.POST['playerNumber']
		playerPosition = request.POST['playerPosition']
		playerNationality = request.POST['playerNationality']
		
		playerImage = request.FILES['playerImage']
		fss = FileSystemStorage()
		file = fss.save(playerImage.name, playerImage)
		file_url = fss.url(file)

		print(file_url)

		fplayer = Football_Player(
			player_name=playerName, 
			player_number=playerNumber, 
			player_position=playerPosition, 
			player_nationality=playerNationality, 
			player_image=file_url
		)
		fplayer.save()
	fplayers = Football_Player.objects.all()
	context['players'] = fplayers
	return redirect("TeamsF.html", context=context)

def removeFootballPlayer(request):
	context={}
	arr = []
	if request.method == "POST":
		for key in request.POST.keys():
			arr.append(key)
		removeBtn = arr[1]
		print(removeBtn)
		fplayerdelete = Football_Player.objects.get(id=removeBtn)
		fplayerdelete.delete()
	fplayers = Football_Player.objects.all()
	context['players'] = fplayers
	return redirect("TeamsF.html", context=context)

def updateFootballPlayer(request):
	context={}
	arr = []
	if request.method == "POST":
		
		playerId = request.POST["updateBtn"]
		playerName = request.POST['playerName']
		playerNumber = request.POST['playerNumber']
		playerPosition = request.POST['playerPosition']
		playerNationality = request.POST['playerNationality']
		print([playerId, playerName, playerNumber, playerPosition, playerNationality])


		print("BREAK")
		print(request.FILES['playerImage'])
		# if request.FILES['playerImage'] != None:
		# 	playerImage = request.FILES['playerImage']
		# 	fss = FileSystemStorage()
		# 	file = fss.save(playerImage.name, playerImage)
		# 	file_url = fss.url(file)

		# 	bplayerupdate = Basketball_Player(
		# 		id=playerId, 
		# 		player_name=playerName, 
		# 		player_number=playerNumber, 
		# 		player_position=playerPosition, 
		# 		player_nationality=playerNationality, 
		# 		player_image=file_url
		# 		)

		# 	bplayerupdate.save()
			
		# else:
		fplayerupdate = Football_Player.objects.filter(id=playerId)
		
		fplayerupdate.update(
			player_name=playerName, 
			player_number=playerNumber, 
			player_position=playerPosition, 
			player_nationality=playerNationality, 
		)

	fplayers = Football_Player.objects.all()
	context['players'] = fplayers
	return redirect("TeamsF.html", context=context)


# BASKTEBALL TICKETS

def buyBasketballTicket(request):
	context={}
	arr = []
	if request.method == "POST":
		for key in request.POST.keys():
			arr.append(key)
		buyBtn = arr[1]
		print("HAHAHAHAHAHA")
		print(buyBtn)
		print("HAHAHAHAHAHA")
		userId = request.session.get('_auth_user_id')
		print(userId)
		basketballBought = Basketball_Bought_Ticket(basketball_bought_ticket_id=buyBtn, username_id=userId)
		basketballBought.save()
		
		profiles = Profile.objects.all()
		for profile in profiles:
			if int(profile.username_id) == int(userId):
				profileBalance = profile.balance
				print(profileBalance)

		basketballTickets = Basketball_Ticket.objects.all()
		for ticket in basketballTickets:
			if int(ticket.id) == int(buyBtn):
				basketballTicketPrice = ticket.basketball_ticket_price
				print(basketballTicketPrice)

		newBalance = profileBalance - basketballTicketPrice

		for profile in profiles:
			if int(profile.username_id) == int(userId):
				profile.balance = newBalance
				profile.save()

		btickets = Basketball_Ticket.objects.all()
		for bticket in btickets:
			if int(bticket.id) == int(buyBtn):
				bticket.basketball_ticket_count = bticket.basketball_ticket_count - 1
				bticket.save()
		

	btickets = Basketball_Ticket.objects.all()
	context['btickets'] = btickets
	return redirect("Tickets.html", context=context)



# FOR ACCOUNTS AND PROFILE

def changeProfileImage(request):
	context={}
	if request.method == "POST":
		print("CHECKKKK")
		userId = request.session.get('_auth_user_id')
		profileupdate = Profile.objects.filter(username_id=userId)

		roundimgExist = request.FILES.get('profileImage', False)
		backimgExist = request.FILES.get('profileBackgroundImage', False)
		fss = FileSystemStorage()

		if (roundimgExist) and not(backimgExist):
			roundimg = request.FILES['profileImage']
			if fss.exists(roundimg.name):
				file1_url = fss.url(roundimg.name)
				profileupdate.update(
					userimage=file1_url
				)
			else:
				print("INHEREEEEEEE1111")
				file1 = fss.save(roundimg.name, roundimg)
				file1_url = fss.url(file1)
				profileupdate.update(
					userimage=file1_url
				)

		elif (backimgExist) and not(roundimgExist):
			backimg = request.FILES['profileBackgroundImage']
			if fss.exists(backimg.name):
				file2_url = fss.url(backimg.name)
				profileupdate.update(
					userbackimage=file2_url
				)
			else:
				print("INHEREEEEEEE2222")
				file2 = fss.save(backimg.name, backimg)
				file2_url = fss.url(file2)
				profileupdate.update(
					userbackimage=file2_url
				)
		elif (backimgExist) and (roundimgExist):
			roundimg = request.FILES['profileImage']
			backimg = request.FILES['profileBackgroundImage']
			if fss.exists(roundimg.name) and fss.exists(backimg.name):
				file1_url = fss.url(roundimg.name)
				file2_url = fss.url(backimg.name)
				profileupdate.update(
					userimage=file1_url,
					userbackimage=file2_url
				)
			else:
				print("INHEREEEEEEE33333")
				file1 = fss.save(roundimg.name, roundimg)
				file1_url = fss.url(file1)
				file2 = fss.save(backimg.name, backimg)
				file2_url = fss.url(file2)
				profileupdate.update(
					userimage=file1_url,
					userbackimage=file2_url
				)
		else:
			print("NOT WORKING")
			profiles = Profile.objects.all()
			context['profile'] = profiles
			return redirect("userProfile.html", context=context)

	profiles = Profile.objects.all()
	context['profile'] = profiles
	return redirect("userProfile.html", context=context)



def deleteAccount(request):
	if request.method == "POST":
		userId = request.session.get('_auth_user_id')
		userDelete = User.objects.get(id = userId)
		userDelete.delete()
		request.session.flush()
		messages.success(request, "The user is deleted!")
		return redirect("/")



###############################################################################################

def Home(request):
	context={}
	if request.method == 'GET':
		profiles = Profile.objects.all()
		context['profiles'] = profiles
		return render(request, 'Home.html', context)


def About(request):
	context={}
	profiles = Profile.objects.all()
	context['profiles'] = profiles
	return render(request, 'About.html', context)


def StadiumMuseum(request):
	context={}
	profiles = Profile.objects.all()
	context['profiles'] = profiles
	return render(request, 'StadiumMuseum.html', context)


def TeamsB(request):
	context={}
	if request.method == 'GET':
		bplayers = Basketball_Player.objects.all()
		context['players'] = bplayers
		profiles = Profile.objects.all()
		context['profiles'] = profiles
		return render(request, 'TeamsB.html', context)


def TeamsF(request):
	context={}
	if request.method == 'GET':
		fplayers = Football_Player.objects.all()
		context['players'] = fplayers
		profiles = Profile.objects.all()
		context['profiles'] = profiles
		return render(request, 'TeamsF.html', context)
			
			# else:
			#     messages.error(request, 'Player sport type was not chosen.') 
		

def Fixtures(request):
	context={}
	if request.method == 'GET':
		ftickets = Football_Ticket.objects.all()
		btickets = Basketball_Ticket.objects.all()
		context["ftickets"] = ftickets
		context["btickets"] = btickets
		profiles = Profile.objects.all()
		context['profiles'] = profiles
		return render(request, 'Fixtures.html', context)
	

def Tickets(request):
	context={}
	if request.method == 'GET':
		ftickets = Football_Ticket.objects.all()
		btickets = Basketball_Ticket.objects.all()
		context["ftickets"] = ftickets
		context["btickets"] = btickets
		profiles = Profile.objects.all()
		context['profiles'] = profiles
		return render(request, 'Tickets.html', context)
	if request.method == 'POST':
		ftickets = Football_Ticket.objects.all()
		context["ftickets"] = ftickets

		session_user_id = request.session.get('_auth_user_id')
		ticket_price = request.session.get('')
		print(ticket_price)
		# update_profile = Profile.objects.filter(username_id=session_user_id)
		# update_profile.update(balance=update_profile.balance - )
		return render(request, 'Tickets.html', context)
	


def Shop(request):
	context={}
	profiles = Profile.objects.all()
	context['profiles'] = profiles
	return render(request, 'Shop.html', context)

def News(request):
	context={}
	profiles = Profile.objects.all()
	context['profiles'] = profiles
	return render(request, 'News.html', context)    

def userProfile(request):
	context={}
	profiles = Profile.objects.all()
	context['profiles'] = profiles
	return render(request, 'userProfile.html', context)