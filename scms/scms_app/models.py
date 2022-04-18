from django.db import models
from django.contrib.auth.models import User

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

class Ticket(models.Model):
    ticket_opponent = models.CharField(max_length=100)
    ticket_homeaway = models.CharField(max_length=100 ,choices=HOMEAWAY)
    ticket_location = models.CharField(max_length=100)
    ticket_date = models.DateTimeField()
    ticket_price = models.IntegerField()
    ticket_count = models.IntegerField()
    ticket_image = models.ImageField(upload_to="static/scms_app/images")

    def __str__(self):
        return self.ticket_opponent

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"

class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField()

    def __str__(self):
        return str(self.username)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"