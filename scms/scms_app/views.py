from django.shortcuts import render


def Home(request):
    return render(request, 'Home.html', {})


def About(request):
    return render(request, 'About.html', {})


def Signin(request):
    return render(request, 'Signin.html', {})


def Signup(request):
    return render(request, 'Signup.html', {})


def StadiumMuseum(request):
    return render(request, 'StadiumMuseum.html', {})
