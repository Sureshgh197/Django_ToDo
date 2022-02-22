from django.contrib import admin

# Register your models here.\
from .models import Task,Category,RecycleBin
# Register your models here.
admin.site.register(Task)
admin.site.register(Category)
admin.site.register(RecycleBin)
