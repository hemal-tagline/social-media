from django.contrib import admin
from  django.contrib.auth.models  import  Group
# Register your models here.
from .models import *


class DetailsAdmin(admin.ModelAdmin):
    list_display=('book_name','category','Author','pages')

class AuthorAdmin(admin.ModelAdmin):
    list_display=['name','image_tag']
    list_display_links = ['name','image_tag']

admin.site.register(Category)
admin.site.register(Details,DetailsAdmin)
# admin.site.register(Publisher)
admin.site.register(Author,AuthorAdmin)

admin.site.unregister(Group)