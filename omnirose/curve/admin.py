from django.contrib import admin
from .models import Curve, Reading

class CurveAdmin(admin.ModelAdmin):
    pass

class ReadingAdmin(admin.ModelAdmin):
    pass

admin.site.register(Curve, CurveAdmin)
admin.site.register(Reading, ReadingAdmin)
