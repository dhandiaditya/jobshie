from django.contrib import admin
from .models import User, Jobseeker, Company

admin.site.register(User)
admin.site.register(Jobseeker)
admin.site.register(Company)