from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Post, User , PushNotification
from import_export.admin import ExportMixin, ImportExportModelAdmin , ImportMixin
from django.contrib import messages
from django.utils.translation import ngettext
# Only Export For used -> ExportMixin
# Only Import For used -> ImportMixin
from .models import MapHistory, ExcelFilesUpload 
from mapbox_location_field.admin import MapAdmin
from django.contrib.auth.hashers import make_password

class UserAdmin(ImportExportModelAdmin , admin.ModelAdmin):
    list_display = ['id','first_name','last_name','email','device_type','provider_type','is_superuser' ]
    fields = [ 'first_name','last_name','email', 'password', 'is_superuser','device_type','provider_type','device_id','provider_user_id']
    exclude = ('groups', 'created_at', 'is_staff', 'user_permissions', 'date_joined', 'last_login', 'is_active')
    search_fields = ('email',)
    readonly_fields=('device_id','provider_user_id')
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['device_type']
        else:
            return []
    list_display_links = None
    actions = ['device_type']
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

    @admin.action(description='Mark selected device_type as Default Android')
    def device_type(self, request, queryset):
        updated = queryset.update(device_type='android')
        self.message_user(request, ngettext(
            '%d device type was successfully marked as Android.',
            '%d device type were successfully marked as Android.',
            updated,
        ) % updated, messages.SUCCESS)
        
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    ''' User Module
        If True is show on admin panel and else is don't show
        If You Have Don't have in Admin Panel And any time access only url Link
        http://127.0.0.1:8000/admin/user/user/
    '''
    def has_module_permission(self, request, obj=None):
        return True
    
    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser == False:
            return obj is None or Post.objects.filter(user=request.user.pk)
    
    def get_queryset(self, request):
        if request.user.is_superuser == False:        
            return User.objects.filter(pk=request.user.pk)
        else:
            return User.objects.all()
    
    # def has_view_permission(self, request, obj=None):
    #     return False
    # admin.site.disable_action('delete_selected')
    
class MapHistoryAdmin(admin.ModelAdmin):
    list_display = ["id","destination_latitude","destination_longitude"]
    
class ExcelFilesUploadAdmin(admin.ModelAdmin):
    list_display = ["id","Files"]
        
class PostAdmin(admin.ModelAdmin):
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['user']
        else:
            return []

    list_display = ['id','name','description','user']

    fieldsets = [
        (None, { 'fields': ('name','description') } ),
    ]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj.save()

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser == False:
            return obj is None or Post.objects.filter(user=request.user.pk)
        
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser == False:
            return obj is None or Post.objects.filter(user=request.user.pk)
        else:
            return True
        
    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request, obj=None):
        return True
    
    def get_queryset(self, request):
        if request.user.is_superuser == False:        
            return Post.objects.filter(user=request.user.pk)
        else:
            return Post.objects.all()

admin.site.register(User ,UserAdmin)
admin.site.register(PushNotification)
admin.site.register(MapHistory, MapHistoryAdmin)
admin.site.register(ExcelFilesUpload,ExcelFilesUploadAdmin)
admin.site.register(Post,PostAdmin)