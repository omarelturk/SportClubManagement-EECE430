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
    path('Fixtures.html', views.Fixtures, name='Fixtures'),
    path('Tickets.html', views.Tickets, name='Tickets'),
    path('Shop.html', views.Shop, name='Shop'),
    path('News.html', views.News, name='News'),
    path('userProfile.html', views.userProfile, name='userProfile'),
    path('addBasketballPlayer', views.addBasketballPlayer, name='addBasketballPlayer'),
    path('removeBasketballPlayer', views.removeBasketballPlayer, name='removeBasketballPlayer'),
    path('updateBasketballPlayer', views.updateBasketballPlayer, name='updateBasketballPlayer'),
    path('addFootballPlayer', views.addFootballPlayer, name='addFootballPlayer'),
    path('removeFootballPlayer', views.removeFootballPlayer, name='removeFootballPlayer'),
    path('updateFootballPlayer', views.updateFootballPlayer, name='updateFootballPlayer'),
    path('buyBasketballTicket', views.buyBasketballTicket, name='buyBasketballTicket'),
    path('changeProfileImage', views.changeProfileImage, name='changeProfileImage'),
    path('deleteAccount', views.deleteAccount, name='deleteAccount'),
    # path('getBasketballPlayerId', views.getBasketballPlayerId, name='getBasketballPlayerId'),
]
