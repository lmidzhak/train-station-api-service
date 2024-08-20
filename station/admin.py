from django.contrib import admin

from .models import (
    TrainType,
    Train,
    Station,
    Route,
    CrewMember,
    Journey,
    Ticket,
    Order,
)

admin.site.register(TrainType)
admin.site.register(Train)
admin.site.register(Station)
admin.site.register(Route)
admin.site.register(CrewMember)
admin.site.register(Journey)
admin.site.register(Ticket)
admin.site.register(Order)
