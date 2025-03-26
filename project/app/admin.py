from django.contrib import admin
from  .models import *

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Department)
admin.site.register(Payment)
admin.site.register(Booking)
admin.site.register(Customer)
admin.site.register(Staf)

