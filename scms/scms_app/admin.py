from django.contrib import admin
from scms_app.models import Football_Player, Basketball_Player, Ticket, Profile

# Register your models here.

admin.site.register(Football_Player)
admin.site.register(Basketball_Player)
admin.site.register(Ticket)
admin.site.register(Profile)