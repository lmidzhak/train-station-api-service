from django.contrib import admin

from .models import (
    TrainType,
    Train,
    Station,
    Route,
)

admin.site.register(TrainType)
admin.site.register(Train)
admin.site.register(Station)
admin.site.register(Route)
