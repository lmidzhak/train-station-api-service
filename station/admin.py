from django.contrib import admin

from models import (
    TrainType,
    Train,
)

admin.site.register(TrainType)
admin.site.register(Train)
