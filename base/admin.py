from django.contrib import admin
from .models import User, Event, Organizer, Receipt, Ticket, TicketType, Feedback

admin.site.register(User)
admin.site.register(Event)
admin.site.register(Organizer)
admin.site.register(Receipt)
admin.site.register(Ticket)
admin.site.register(TicketType)
admin.site.register(Feedback)
