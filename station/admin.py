from django.contrib import admin

from .models import (
    TrainType,
    Train,
    Station,
    Route,
    Crew,
)

admin.site.register(TrainType)
admin.site.register(Train)
admin.site.register(Station)
admin.site.register(Route)
admin.site.register(Crew)
