from django.contrib import admin

# Register your models here.
from .models import Profile, Contact

admin.site.register([Profile, Contact])
