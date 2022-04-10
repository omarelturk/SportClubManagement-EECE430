from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='Home'),
    path('About.html', views.About, name='About'),
    path('Signin.html', views.Signin, name='Signin'),
    path('Signup.html', views.Signup, name='Signup'),
    path('StadiumMuseum.html', views.StadiumMuseum, name='StadiumMuseum'),
]
