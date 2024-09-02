from django.contrib import admin
from app.models import Item

# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    model = Item

admin.site.register(Item, ItemAdmin)