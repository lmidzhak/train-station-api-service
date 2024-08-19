from django.contrib import admin

from .models import (
    TrainType,
    Train,
    Station,
)

admin.site.register(TrainType)
admin.site.register(Train)
admin.site.register(Station)
