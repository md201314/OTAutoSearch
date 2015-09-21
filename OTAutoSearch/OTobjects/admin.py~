from django.contrib import admin
from OTobjects.models import OTuniq, OTcands, Catfiles

# Register your models here.
class OTuniqAdmin(admin.ModelAdmin):
    list_display = ["OTid","x","y"]
class OTcandsAdmin(admin.ModelAdmin):
    list_display = ["OTid","Catid","x","y"]
class CatfilesAdmin(admin.ModelAdmin):
    list_display = ["Catid","JD"]

admin.site.register(OTuniq,OTuniqAdmin)
admin.site.register(OTcands,OTcandsAdmin)
admin.site.register(Catfiles)

