from django.contrib import admin
from .models import founderregisration, investorregistration
from .models import *
# Register your models here.
admin.site.register(founderregisration)
admin.site.register(investorregistration)
admin.site.register(registration)
admin.site.register(Startup)
admin.site.register(Paymentmodel)