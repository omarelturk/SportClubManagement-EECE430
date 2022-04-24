from django.contrib import admin
from scms_app.models import Football_Player, Basketball_Player, Football_Ticket, Basketball_Ticket, Profile, Football_Bought_Ticket, Basketball_Bought_Ticket

# Register your models here.

admin.site.register(Profile)
admin.site.register(Football_Player)
admin.site.register(Basketball_Player)
admin.site.register(Football_Ticket)
admin.site.register(Basketball_Ticket)
admin.site.register(Football_Bought_Ticket)
admin.site.register(Basketball_Bought_Ticket)