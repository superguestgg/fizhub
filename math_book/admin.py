from django.contrib import admin
from .models import Subject, University, Ticket, Guest, Session,\
    Guest_session, Vote_ticket, Theorem, Vote_theorem, Definition,\
    Vote_definition
admin.site.register(Subject)
admin.site.register(University)
admin.site.register(Ticket)
admin.site.register(Guest)
admin.site.register(Session)
admin.site.register(Guest_session)
admin.site.register(Vote_ticket)
admin.site.register(Theorem)
admin.site.register(Vote_theorem)
admin.site.register(Definition)
admin.site.register(Vote_definition)


# Register your models here.
