from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home, name='Home'),
    path('About.html', views.About, name='About'),
    path('Signin.html', views.login_request, name='Signin'),
    path('Signup.html', views.register_request, name='Signup'),
    path('logout', views.logout_request, name= 'logout'),
    path('passwordreset', views.password_reset_request, name="passwordreset"),
    path('StadiumMuseum.html', views.StadiumMuseum, name='StadiumMuseum'),
    path('TeamsB.html', views.TeamsB, name='TeamsB'),
    path('TeamsF.html', views.TeamsF, name='TeamsF'),
    #path("register", views.register_request, name="register")
    # path('/login', views.LoginView.as_view(template_name="scms_app/templates/Signin.html"), name='login'),
    # path('/logout', views.LogoutView.as_view(), name='logout')
]
