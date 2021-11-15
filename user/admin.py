from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User , PushNotification
from import_export.admin import ExportMixin, ImportExportModelAdmin , ImportMixin

# Only Export For used -> ExportMixin
# Only Import For used -> ImportMixin
from .models import MapHistory  
from mapbox_location_field.admin import MapAdmin  

class UserAdmin(ImportExportModelAdmin , admin.ModelAdmin):
    list_display = ['id','first_name','last_name','email','device_type','provider_type','is_superuser' ]
    fields = [ 'first_name','last_name','email', 'password', 'is_superuser','device_type','provider_type','device_id','provider_user_id']
    exclude = ('groups', 'created_at', 'is_staff', 'user_permissions', 'date_joined', 'last_login', 'is_active')
    search_fields = ('email',)
    readonly_fields=('device_id','provider_user_id')

    def get_email(self, obj):
        return obj.email if obj.email else "Guest user"
    get_email.short_description = "Email"

    def save_model(self, request, obj, form, change):
        # Override this to set the password to the value in the field if it's
        obj.is_staff = True
        if obj.pk:
            orig_obj = User.objects.get(pk=obj.pk)
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)
        obj.save()
        
class MapHistoryAdmin(admin.ModelAdmin):
    list_display = ["id","destination_latitude","destination_longitude"]
        
admin.site.register(User ,UserAdmin)
admin.site.register(PushNotification)
admin.site.register(MapHistory, MapHistoryAdmin)  