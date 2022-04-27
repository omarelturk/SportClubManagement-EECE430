#from multiprocessing import context
from multiprocessing import context
from os import stat
from re import M
from django.shortcuts import render, redirect
from django.urls import resolve
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from platformdirs import user_documents_dir
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
from scms_app.models import Football_Player, Basketball_Player, Football_Ticket, Basketball_Ticket, Profile, Merchandise, SportsNews
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
		file_url = None
		form = NewUserForm(request.POST, request.FILES)
		user_select = request.POST["users_type"]
		if user_select == "normaluser":
			if form.is_valid():
				formusername = form.cleaned_data.get('username')
				formaddress = form.cleaned_data.get('address')
				form.save()

				print(formusername)

				print("LOOOK HHEREEEEEE")
				print(request.FILES)
				print("AFTERRRRR")

				fss = FileSystemStorage()
				userImageExist = request.FILES.get('userImage', False)

				if userImageExist:
					userImage = request.FILES['userImage']
					if fss.exists(userImage.name):
						print(userImage)
						file_url = fss.url(userImage.name)
					else:
						print(userImage)
						file = fss.save(userImage.name, userImage)
						file_url = fss.url(file)

				user = User.objects.get(username=formusername.lower())

				if file_url is None:
					profile = Profile(username_id=user.id, user_name=user.username, address=formaddress, balance=0)
					profile.save()
				else:
					profile = Profile(username_id=user.id, user_name=user.username, userimage=file_url, address=formaddress, balance=0)
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
		playerImageExist = request.FILES.get('playerImage', False)

		if playerImageExist:
			playerImage = request.FILES['playerImage']
			if fss.exists(playerImage.name):
				file1_url = fss.url(playerImage.name)
				bplayers = Basketball_Player(
					player_name=playerName, 
					player_number=playerNumber, 
					player_position=playerPosition, 
					player_nationality=playerNationality, 
					player_image=file1_url
				)
			else:
				print("INHEREEEEEEE1111")
				file1 = fss.save(playerImage.name, playerImage)
				file1_url = fss.url(file1)
				bplayers = Basketball_Player(
					player_name=playerName, 
					player_number=playerNumber, 
					player_position=playerPosition, 
					player_nationality=playerNationality, 
					player_image=file1_url
				)

		bplayers.save()

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
	if request.method == "POST":
		
		playerId = request.POST["updateBtn"]
		playerName = request.POST['playerName']
		playerNumber = request.POST['playerNumber']
		playerPosition = request.POST['playerPosition']
		playerNationality = request.POST['playerNationality']
		print([playerId, playerName, playerNumber, playerPosition, playerNationality])


		print("BREAK")
		print(request.FILES['playerImage'])
		bplayerupdate = Basketball_Player.objects.filter(id=playerId)

		playerImageExist = request.FILES.get('playerImage', False)
		fss = FileSystemStorage()

		if playerImageExist:
			playerImage = request.FILES['playerImage']
			if fss.exists(playerImage.name):
				file1_url = fss.url(playerImage.name)
				bplayerupdate.update(
					player_name=playerName, 
					player_number=playerNumber, 
					player_position=playerPosition, 
					player_nationality=playerNationality, 
					player_image=file1_url
				)
			else:
				print("INHEREEEEEEE1111")
				file1 = fss.save(playerImage.name, playerImage)
				file1_url = fss.url(file1)
				bplayerupdate.update(
					player_name=playerName, 
					player_number=playerNumber, 
					player_position=playerPosition, 
					player_nationality=playerNationality, 
					player_image=file1_url
				)
		else:
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
		playerImageExist = request.FILES.get('playerImage', False)

		fss = FileSystemStorage()
		if playerImageExist:
			playerImage = request.FILES['playerImage']
			if fss.exists(playerImage.name):
				file1_url = fss.url(playerImage.name)
				fplayers = Football_Player(
					player_name=playerName, 
					player_number=playerNumber, 
					player_position=playerPosition, 
					player_nationality=playerNationality, 
					player_image=file1_url
				)
			else:
				print("INHEREEEEEEE1111")
				file1 = fss.save(playerImage.name, playerImage)
				file1_url = fss.url(file1)
				fplayers = Football_Player(
					player_name=playerName, 
					player_number=playerNumber, 
					player_position=playerPosition, 
					player_nationality=playerNationality, 
					player_image=file1_url
				)

		fplayers.save()

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
	if request.method == "POST":
		
		playerId = request.POST["updateBtn"]
		playerName = request.POST['playerName']
		playerNumber = request.POST['playerNumber']
		playerPosition = request.POST['playerPosition']
		playerNationality = request.POST['playerNationality']
		print([playerId, playerName, playerNumber, playerPosition, playerNationality])


		print("BREAK")

		fplayerupdate = Football_Player.objects.filter(id=playerId)

		playerImageExist = request.FILES.get('playerImage', False)
		fss = FileSystemStorage()

		if playerImageExist:
			playerImage = request.FILES['playerImage']
			if fss.exists(playerImage.name):
				file1_url = fss.url(playerImage.name)
				fplayerupdate.update(
					player_name=playerName, 
					player_number=playerNumber, 
					player_position=playerPosition, 
					player_nationality=playerNationality, 
					player_image=file1_url
				)
			else:
				print("INHEREEEEEEE1111")
				file1 = fss.save(playerImage.name, playerImage)
				file1_url = fss.url(file1)
				fplayerupdate.update(
					player_name=playerName, 
					player_number=playerNumber, 
					player_position=playerPosition, 
					player_nationality=playerNationality, 
					player_image=file1_url
				)
		else:
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

		profiles = Profile.objects.all()

		for profile in profiles:
			if int(profile.username_id) == int(userId):
				profileBalance = profile.balance
				profileUsername = profile.user_name
				print(profileBalance)
				print(profileUsername)

		basketballTickets = Basketball_Ticket.objects.all()

		for ticket in basketballTickets:
			if int(ticket.id) == int(buyBtn):
				basketballTicketPrice = ticket.basketball_ticket_price
				print(basketballTicketPrice)

		if profileBalance >= basketballTicketPrice:
			newBalance = profileBalance - basketballTicketPrice
		else:
			messages.error(request, 'Insufficient Balance. Please head to your Profile page to add credit into the account.')
			btickets = Basketball_Ticket.objects.all()
			context['btickets'] = btickets
			return redirect("Tickets.html", context=context)

		basketballBought = Basketball_Bought_Ticket(basketball_bought_ticket_id=buyBtn, username_id=userId, user_name=profileUsername)
		basketballBought.save()

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

def addBasketballTicket(request):
	context={}
	if request.method == "POST":
		opponent_name = request.POST['opponentName']
		match_location = request.POST['matchLocation']
		ticket_price = request.POST['ticketPrice']
		available_tickets = request.POST['availableTickets']
		match_date = request.POST['matchDate']

		opponentImageExist = request.FILES.get('opponentImage', False)
		fss = FileSystemStorage()

		if opponentImageExist:
			opponent_image = request.FILES['opponentImage']
			if fss.exists(opponent_image.name):
				file1_url = fss.url(opponent_image.name)
				newbtickets = Basketball_Ticket(
					basketball_ticket_opponent=opponent_name,
					basketball_ticket_location=match_location,
					basketball_ticket_date=match_date,
					basketball_ticket_price=ticket_price,
					basketball_ticket_count=available_tickets,
					basketball_ticket_image=file1_url,
				)
				newbtickets.save()
			else:
				print("INHEREEEEEEE1111")
				file1 = fss.save(opponent_image.name, opponent_image)
				file1_url = fss.url(file1)
				newbtickets = Basketball_Ticket(
					basketball_ticket_opponent=opponent_name,
					basketball_ticket_location=match_location,
					basketball_ticket_date=match_date,
					basketball_ticket_price=ticket_price,
					basketball_ticket_count=available_tickets,
					basketball_ticket_image=file1_url,
				)
				newbtickets.save()

	btickets = Basketball_Ticket.objects.all()
	context['btickets'] = btickets
	return redirect("Tickets.html", context=context)

def removeBasketballTicket(request):
	context={}
	arr = []
	if request.method == "POST":
		for key in request.POST.keys():
			arr.append(key)
		removeBtn = arr[1]
		print(removeBtn)
		bticketdelete = Basketball_Ticket.objects.get(id=removeBtn)
		bticketdelete.delete()
	btickets = Basketball_Ticket.objects.all()
	context['btickets'] = btickets
	return redirect("Tickets.html", context=context)

def updateBasketballTicket(request):
	context={}
	if request.method == "POST":

		ticketId = request.POST["updateBtn"]		
		opponent_name = request.POST['opponentName']
		match_location = request.POST['matchLocation']
		ticket_price = request.POST['ticketPrice']
		available_tickets = request.POST['availableTickets']
		match_date = request.POST['matchDate']
		
		print("BREAK")

		bticketupdate = Basketball_Ticket.objects.filter(id=ticketId)

		opponentImageExist = request.FILES.get('opponentImage', False)
		fss = FileSystemStorage()

		if opponentImageExist:
			opponentImage = request.FILES['opponentImage']
			if fss.exists(opponentImage.name):
				file1_url = fss.url(opponentImage.name)
				bticketupdate.update(
					basketball_ticket_opponent=opponent_name,
					basketball_ticket_location=match_location,
					basketball_ticket_date=match_date,
					basketball_ticket_price=ticket_price,
					basketball_ticket_count=available_tickets,
					basketball_ticket_image=file1_url,
				)
			else:
				print("INHEREEEEEEE1111")
				file1 = fss.save(opponentImage.name, opponentImage)
				file1_url = fss.url(file1)
				bticketupdate.update(
					basketball_ticket_opponent=opponent_name,
					basketball_ticket_location=match_location,
					basketball_ticket_date=match_date,
					basketball_ticket_price=ticket_price,
					basketball_ticket_count=available_tickets,
					basketball_ticket_image=file1_url,
				)
		else:
			bticketupdate.update(
				basketball_ticket_opponent=opponent_name,
					basketball_ticket_location=match_location,
					basketball_ticket_date=match_date,
					basketball_ticket_price=ticket_price,
					basketball_ticket_count=available_tickets,
			)

	btickets = Basketball_Ticket.objects.all()
	context['btickets'] = btickets
	return redirect("Tickets.html", context=context)




# FOOTBALL TICKETS

def buyFootballTicket(request):
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

		profiles = Profile.objects.all()
		for profile in profiles:
			if int(profile.username_id) == int(userId):
				profileBalance = profile.balance
				profileUsername = profile.user_name
				print(profileBalance)
				print(profileUsername)

		footballTickets = Football_Ticket.objects.all()
		for ticket in footballTickets:
			if int(ticket.id) == int(buyBtn):
				footballTicketPrice = ticket.football_ticket_price
				print(footballTicketPrice)
		if profileBalance >= footballTicketPrice:
			newBalance = profileBalance - footballTicketPrice
		else:
			messages.error(request, 'Insufficient Balance. Please head to your Profile page to add credit into the account.')
			ftickets = Football_Ticket.objects.all()
			context['ftickets'] = ftickets
			return redirect("Tickets.html", context=context)

		footballBought = Football_Bought_Ticket(football_bought_ticket_id=buyBtn, username_id=userId, user_name=profileUsername)
		footballBought.save()
		

		for profile in profiles:
			if int(profile.username_id) == int(userId):
				profile.balance = newBalance
				profile.save()

		ftickets = Football_Ticket.objects.all()
		for fticket in ftickets:
			if int(fticket.id) == int(buyBtn):
				fticket.football_ticket_count = fticket.football_ticket_count - 1
				fticket.save()
		

	ftickets = Football_Ticket.objects.all()
	context['ftickets'] = ftickets
	return redirect("Tickets.html", context=context)

def addFootballTicket(request):
	context={}
	if request.method == "POST":
		opponent_name = request.POST['opponentName']
		match_location = request.POST['matchLocation']
		home_away = request.POST['homeAway']
		ticket_price = request.POST['ticketPrice']
		available_tickets = request.POST['availableTickets']
		match_date = request.POST['matchDate']

		opponentImageExist = request.FILES.get('opponentImage', False)
		fss = FileSystemStorage()

		if opponentImageExist:
			opponent_image = request.FILES['opponentImage']
			if fss.exists(opponent_image.name):
				file1_url = fss.url(opponent_image.name)
				newftickets = Football_Ticket(
					football_ticket_opponent=opponent_name,
					football_ticket_homeaway=home_away,
					football_ticket_location=match_location,
					football_ticket_date=match_date,
					football_ticket_price=ticket_price,
					football_ticket_count=available_tickets,
					football_ticket_image=file1_url,
				)
				newftickets.save()
			else:
				print("INHEREEEEEEE1111")
				file1 = fss.save(opponent_image.name, opponent_image)
				file1_url = fss.url(file1)
				newftickets = Football_Ticket(
					football_ticket_opponent=opponent_name,
					football_ticket_homeaway=home_away,
					football_ticket_location=match_location,
					football_ticket_date=match_date,
					football_ticket_price=ticket_price,
					football_ticket_count=available_tickets,
					football_ticket_image=file1_url,
				)
				newftickets.save()

	ftickets = Football_Ticket.objects.all()
	context['ftickets'] = ftickets
	return redirect("Tickets.html", context=context)

def removeFootballTicket(request):
	context={}
	arr = []
	if request.method == "POST":
		for key in request.POST.keys():
			arr.append(key)
			print(key)
		removeBtn = arr[1]
		print(removeBtn)
		fticketdelete = Football_Ticket.objects.get(id=removeBtn)
		fticketdelete.delete()
	ftickets = Football_Ticket.objects.all()
	context['ftickets'] = ftickets
	return redirect("Tickets.html", context=context)


def updateFootballTicket(request):
	context={}
	arr=[]
	if request.method == "POST":

		ticketId = request.POST["updateBtn"]		
		opponent_name = request.POST['opponentName']
		match_location = request.POST['matchLocation']
		home_away = request.POST['homeAway']
		ticket_price = request.POST['ticketPrice']
		available_tickets = request.POST['availableTickets']
		match_date = request.POST['matchDate']

		

		print("BREAK")

		fticketupdate = Football_Ticket.objects.filter(id=ticketId)

		opponentImageExist = request.FILES.get('opponentImage', False)
		fss = FileSystemStorage()

		if opponentImageExist:
			opponentImage = request.FILES['opponentImage']
			if fss.exists(opponentImage.name):
				file1_url = fss.url(opponentImage.name)
				fticketupdate.update(
					football_ticket_opponent=opponent_name,
					football_ticket_homeaway=home_away,
					football_ticket_location=match_location,
					football_ticket_date=match_date,
					football_ticket_price=ticket_price,
					football_ticket_count=available_tickets,
					football_ticket_image=file1_url,
				)
			else:
				print("INHEREEEEEEE1111")
				file1 = fss.save(opponentImage.name, opponentImage)
				file1_url = fss.url(file1)
				fticketupdate.update(
					football_ticket_opponent=opponent_name,
					football_ticket_homeaway=home_away,
					football_ticket_location=match_location,
					football_ticket_date=match_date,
					football_ticket_price=ticket_price,
					football_ticket_count=available_tickets,
					football_ticket_image=file1_url,
				)
		else:
			fticketupdate.update(
				football_ticket_opponent=opponent_name,
				football_ticket_homeaway=home_away,
				football_ticket_location=match_location,
				football_ticket_date=match_date,
				football_ticket_price=ticket_price,
				football_ticket_count=available_tickets,
			)

	ftickets = Football_Ticket.objects.all()
	context['ftickets'] = ftickets
	return redirect("Tickets.html", context=context)


# FOR SHOP

def addMerchandise(request):
	context={}
	if request.method == "POST":
		merchName = request.POST['merchName']
		merchQuantity = request.POST['merchQuantity']
		merchPrice = request.POST['merchPrice']
		merchType = request.POST['merchType']

		merchImageExist = request.FILES.get('merchImage', False)
		fss = FileSystemStorage()

		if merchImageExist:
			merchImage = request.FILES['merchImage']
			if fss.exists(merchImage.name):
				file1_url = fss.url(merchImage.name)
				newmerch = Merchandise(
					merch_name=merchName,
					merch_quantity=merchQuantity,
					merch_price=merchPrice,
					merch_type=merchType,
					merch_image=file1_url,
				)
				newmerch.save()
			else:
				print("INHEREEEEEEE1111")
				file1 = fss.save(merchImage.name, merchImage)
				file1_url = fss.url(file1)
				newmerch = Merchandise(
					merch_name=merchName,
					merch_quantity=merchQuantity,
					merch_price=merchPrice,
					merch_type=merchType,
					merch_image=file1_url,
				)
				newmerch.save()

	merchandise = Merchandise.objects.all()
	print(merchandise)
	context['merchandise'] = merchandise
	return redirect("Shop.html", context=context)


def removeMerchandise(request):
	context={}
	arr = []
	if request.method == "POST":
		for key in request.POST.keys():
			arr.append(key)
			print(key)
		removeBtn = arr[1]
		print(removeBtn)
		mechdelete = Merchandise.objects.get(id=removeBtn)
		mechdelete.delete()
	mechandise = Merchandise.objects.all()
	context['mechandise'] = mechandise
	return redirect("Shop.html", context=context)

def updateMerchandise(request):
	context={}
	if request.method == "POST":
		
		print(request.POST)

		merchId = request.POST['updateBtn']
		merchName = request.POST['merchName']
		merchQuantity = request.POST['merchQuantity']
		merchPrice = request.POST['merchPrice']
		merchType = request.POST['merchType']

		

		print("BREAK")

		merchupdate = Merchandise.objects.filter(id=merchId)

		merchImageExist = request.FILES.get('merchImage', False)
		fss = FileSystemStorage()

		if merchImageExist:
			merchImage = request.FILES['merchImage']
			if fss.exists(merchImage.name):
				file1_url = fss.url(merchImage.name)
				merchupdate.update(
					merch_name=merchName,
					merch_quantity=merchQuantity,
					merch_price=merchPrice,
					merch_type=merchType,
					merch_image=file1_url,
				)
			else:
				print("INHEREEEEEEE1111")
				file1 = fss.save(merchImage.name, merchImage)
				file1_url = fss.url(file1)
				merchupdate.update(
					merch_name=merchName,
					merch_quantity=merchQuantity,
					merch_price=merchPrice,
					merch_type=merchType,
					merch_image=file1_url,
				)
		else:
			merchupdate.update(
				merch_name=merchName,
				merch_quantity=merchQuantity,
				merch_price=merchPrice,
				merch_type=merchType,
			)

	merchandise = Merchandise.objects.all()
	context['merchandise'] = merchandise
	return redirect("Shop.html", context=context)


def buyMerchandise(request):
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

		profiles = Profile.objects.all()

		for profile in profiles:
			if int(profile.username_id) == int(userId):
				profileBalance = profile.balance
				profileUsername = profile.user_name
				print(profileBalance)
				print(profileUsername)

		merchandise = Merchandise.objects.all()

		for merch in merchandise:
			if int(merch.id) == int(buyBtn):
				merchPrice = merch.merch_price
				merchName = merch.merch_name
				print(merchPrice)

		if profileBalance >= merchPrice:
			newBalance = profileBalance - merchPrice
		else:
			messages.error(request, 'Insufficient Balance. Please head to your Profile page to add credit into the account.')
			merchandise = Merchandise.objects.all()
			context['merchandise'] = merchandise
			return redirect("Shop.html", context=context)

		merchBought = Merchandise_Bought(
			merch_name_id=buyBtn, 
			username_id=userId, 
			user_name=profileUsername,
			product_name=merchName,
			)
		merchBought.save()

		for profile in profiles:
			if int(profile.username_id) == int(userId):
				profile.balance = newBalance
				profile.save()

		merchandise = Merchandise.objects.all()
		for merch in merchandise:
			if int(merch.id) == int(buyBtn):
				merch.merch_quantity = merch.merch_quantity - 1
				merch.save()

		messages.success(request, "You have successfully purchased from "+merch.merch_type+": "+merch.merch_name+"."+" It will be delivered to your address: "+profile.address+".")
		

	merchandise = Merchandise.objects.all()
	context['merchandise'] = merchandise
	return redirect("Shop.html", context=context)

def boughtMerchandise(request):
	context={}
	bought_merch_ids = []
	print("I'm inside bought merchandise")
	userId = request.session.get('_auth_user_id')
	merchandiseBought = Merchandise_Bought.objects.filter(username_id=userId)
	merchandise = Merchandise.objects.all()

	for merch in merchandise:
		print(merch.id)
		for boughtmerch in merchandiseBought:
			if boughtmerch not in bought_merch_ids:
				bought_merch_ids.append(boughtmerch.merch_name_id)

	for i in boughtmerch:
		if i in bought_merch_ids:
			pass

	print(bought_merch_ids)

	# merchandiseId = Merchandise.objects.filter(id=merch_id)

	print("ah ah ah ah ah")
	# print(merchandiseId)
	print(merchandiseBought)

	# for merch in merchandiseId:

		# if int(merch.id) == int(merch_id):
		# 	merch_name = merch.merch_name
		# 	merch_image = merch.merch_image
		# 	merch_price = merch.merch_price
			
	# context = {"merch_name":merch_name, "merch_image":merch_image, "merch_price":merch_price}
		
	return render(request, "Shop.html", context)


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
			profiles = Profile.objects.all()
			context['profile'] = profiles
			return redirect("userProfile.html", context=context)

	profiles = Profile.objects.all()
	context['profile'] = profiles
	return redirect("userProfile.html", context=context)

def updateProfileInfo(request):
	context={}
	if request.method == "POST":
		profileFName = request.POST['profileFName']
		profileLName = request.POST['profileLName']
		profileEmail = request.POST['profileEmail']
		profileAddress = request.POST['profileAddress']

		userId = request.session.get('_auth_user_id')
		userupdate = User.objects.filter(id=userId)
		profileupdate = Profile.objects.filter(username_id=userId)

		userupdate.update(
			first_name = profileFName,
			last_name = profileLName,
			email = profileEmail,
		)

		profileupdate.update(
			address = profileAddress,
		)
	
	profiles = Profile.objects.all()
	context['profile'] = profiles
	return redirect("userProfile.html", context=context)

def updateUsername(request):
	context={}
	if request.method == "POST":

		newuserName = request.POST['newUsername']

		userId = request.session.get('_auth_user_id')
		userupdate = User.objects.filter(id=userId)
		users = User.objects.all()

		userExist = False
		
		print("request name")
		print(newuserName)
		print("database name")
		print(userupdate[0])
		for existingUser in users:
			if (str(newuserName)).lower() == (str(existingUser)).lower():
				userExist = True

		if userExist is False:
			print('trying to update')
			userupdate.update(
				username = str(newuserName).lower(),
			)
		else:
			messages.error(request, "Username already exists!")
	
	profiles = Profile.objects.all()
	context['profile'] = profiles
	return redirect("userProfile.html", context=context)


def addBalance(request):
	context={}
	if request.method == "POST":
		session_user_id = request.session.get('_auth_user_id')
		print("AAAAAAAAAAAAAAA")
		amount_added = request.POST["amount_added"]
		
		profilebalanceupdate = Profile.objects.filter(username_id=session_user_id)

		for profile in profilebalanceupdate:
			old_balance = int(profile.balance)
			print(old_balance)
			new_balance = old_balance+int(amount_added)
			profilebalanceupdate.update(
				balance=new_balance,
			)
				
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


# FOR NEWS

def addNews(request):
	context={}
	if request.method == "POST":
		news_header = request.POST['news_header']
		news_text = request.POST['news_text']

		newsImageExist = request.FILES.get('news_image', False)
		fss = FileSystemStorage()

		if newsImageExist:
			news_image = request.FILES['news_image']
			if fss.exists(news_image.name):
				file1_url = fss.url(news_image.name)
				latestNews = SportsNews(
					newsHeader=news_header,
					newsImage=file1_url,
					newsText=news_text,
				)
				latestNews.save()
			else:
				print("INHEREEEEEEE1111")
				file1 = fss.save(news_image.name, news_image)
				file1_url = fss.url(file1)
				latestNews = SportsNews(
					newsHeader=news_header,
					newsImage=file1_url,
					newsText=news_text,
				)
				latestNews.save()

	allnews = SportsNews.objects.all()
	context['allnews'] = allnews
	return redirect("News.html", context=context)


def removeNews(request):
	context={}
	arr = []
	if request.method == "POST":
		for key in request.POST.keys():
			arr.append(key)
			print(key)
		removeBtn = arr[1]
		print(removeBtn)
		newsdelete = SportsNews.objects.get(id=removeBtn)
		newsdelete.delete()
	allnews = SportsNews.objects.all()
	context['allnews'] = allnews
	return redirect("News.html", context=context)


def updateNews(request):
	context={}
	if request.method == "POST":
		
		print(request.POST)

		newsId = request.POST['updateBtn']
		news_header = request.POST['news_header']
		news_text = request.POST['news_text']

		

		print("BREAK")

		newsupdate = SportsNews.objects.filter(id=newsId)

		newsImageExist = request.FILES.get('newsImage', False)
		fss = FileSystemStorage()

		if newsImageExist:
			newsImage = request.FILES['newsImage']
			if fss.exists(newsImage.name):
				file1_url = fss.url(newsImage.name)
				newsupdate.update(
					newsHeader=news_header,
					newsImage=file1_url,
					newsText=news_text,
				)
			else:
				print("INHEREEEEEEE1111")
				file1 = fss.save(newsImage.name, newsImage)
				file1_url = fss.url(file1)
				newsupdate.update(
					newsHeader=news_header,
					newsImage=file1_url,
					newsText=news_text,
				)
		else:
			print("Im in else")
			newsupdate.update(
				newsHeader=news_header,
				newsText=news_text,
			)

	allnews = SportsNews.objects.all()
	context['allnews'] = allnews
	return redirect("News.html", context=context)

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
	merchandise = Merchandise.objects.all()
	context['merchandise'] = merchandise
	return render(request, 'Shop.html', context)

def News(request):
	context={}
	profiles = Profile.objects.all()
	allnews = SportsNews.objects.all()
	context['allnews'] = allnews
	context['profiles'] = profiles
	return render(request, 'News.html', context)    

def userProfile(request):
	context={}
	profiles = Profile.objects.all()
	context['profiles'] = profiles
	return render(request, 'userProfile.html', context)