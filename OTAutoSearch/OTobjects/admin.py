from django.contrib import admin
from OTobjects.models import OTuniq, OTcands, Catfiles, Fchart, Comments, Users

# Register your models here.
class OTuniqAdmin(admin.ModelAdmin):
    list_display = ["OTid","x","y","Ra","Dec","magorig","status"]
class OTcandsAdmin(admin.ModelAdmin):
    list_display = ["OTid","Catid","x","y"]
class CatfilesAdmin(admin.ModelAdmin):
    list_display = ["Catid","JD","Catna"]
class FchartAdmin(admin.ModelAdmin):
    list_display = ["id","Catid","OTid","Fname","Fpath"]
class UsersAdmin(admin.ModelAdmin):
    list_display = ["uid","uname","passwd","email_add","first_name","last_name","status"]
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['id','OTid','uid','status','comment','datetime']

admin.site.register(OTuniq,OTuniqAdmin)
admin.site.register(OTcands,OTcandsAdmin)
admin.site.register(Catfiles,CatfilesAdmin)
admin.site.register(Users,UsersAdmin)
admin.site.register(Comments,CommentsAdmin)
