from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from scms_app.storage import OverwriteStorage


POSITION1 = [
    ('Forward', 'Forward'),
    ('Midfielder', 'Midfielder'),
    ('Defender', 'Defender'),
    ('Goalkeeper', 'Goalkeeper'),
]

POSITION2 = [
    ('Forward', 'Forward'),
    ('Center', 'Center'),
    ('Guard', 'Guard'),
]

HOMEAWAY = [
    ('H', 'Home'),
    ('A', 'Away'),
]

# Create your models here.
class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    balance = models.IntegerField(default=0)
    address = models.CharField(max_length=100, default="")
    userimage = models.ImageField(storage=OverwriteStorage(), default="scms_app/media/default-user.jpg")
    userbackimage = models.ImageField(storage=OverwriteStorage(), default="scms_app/media/default-back-user.jpg")

    def __str__(self):
        return str(self.username)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

class Football_Player(models.Model):
    player_name = models.CharField(max_length=100)
    player_number = models.IntegerField()
    player_position = models.CharField(max_length=100, choices=POSITION1)
    player_nationality = models.CharField(max_length=100) 
    player_image = models.ImageField(upload_to="static/scms_app/images")

    def __str__(self):
        return self.player_name

    class Meta:
        verbose_name = "Football_Player"
        verbose_name_plural = "Football_Players"

class Basketball_Player(models.Model):
    player_name = models.CharField(max_length=100)
    player_number = models.IntegerField()
    player_position = models.CharField(max_length=100, choices=POSITION2)
    player_nationality = models.CharField(max_length=100) 
    player_image = models.ImageField(upload_to="static/scms_app/images")

    def __str__(self):
        return self.player_name

    class Meta:
        verbose_name = "Basketball_Player"
        verbose_name_plural = "Basketball_Players"

class Football_Ticket(models.Model):
    football_ticket_opponent = models.CharField(max_length=100)
    football_ticket_homeaway = models.CharField(max_length=100 ,choices=HOMEAWAY)
    football_ticket_location = models.CharField(max_length=100)
    football_ticket_date = models.DateTimeField()
    football_ticket_price = models.IntegerField()
    football_ticket_count = models.IntegerField()
    football_ticket_image = models.ImageField(upload_to="static/scms_app/images")

    def __str__(self):
        return self.football_ticket_opponent

    class Meta:
        verbose_name = "Football_Ticket"
        verbose_name_plural = "Football_Tickets"

class Basketball_Ticket(models.Model):
    basketball_ticket_opponent = models.CharField(max_length=100)
    basketball_ticket_location = models.CharField(max_length=100)
    basketball_ticket_date = models.DateTimeField()
    basketball_ticket_price = models.IntegerField()
    basketball_ticket_count = models.IntegerField()
    basketball_ticket_image = models.ImageField(upload_to="static/scms_app/images")

    def __str__(self):
        return self.basketball_ticket_opponent

    class Meta:
        verbose_name = "Basketball_Ticket"
        verbose_name_plural = "Basketball_Tickets"

class Football_Bought_Ticket(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    football_bought_ticket = models.ForeignKey(Football_Ticket, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)


    def __str__(self):
        return self.football_bought_ticket

    class Meta:
        verbose_name = "Football_Bought_Ticket"
        verbose_name_plural = "Football_Bought_Tickets"

class Basketball_Bought_Ticket(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    basketball_bought_ticket = models.ForeignKey(Basketball_Ticket, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)

    def __str__(self):
        return self.basketball_bought_ticket

    class Meta:
        verbose_name = "Basketball_Bought_Ticket"
        verbose_name_plural = "Basketball_Bought_Tickets"