from django.contrib import admin
from .models import user, Diseases, Medicine
# Register your models here.

admin.site.register(user)
admin.site.register(Diseases)
admin.site.register(Medicine)