from django.contrib import admin

from .models import Order ,DisplayRegularPizza , DisplaySicilianPizza , DisplaySub , DisplayDinnerPlatter , DisplayPasta , DisplaySalad , DisplayTopping

# Register your models here.

admin.site.register(Order)
admin.site.register(DisplayRegularPizza)
admin.site.register(DisplaySicilianPizza)
admin.site.register(DisplaySub)
admin.site.register(DisplayDinnerPlatter)
admin.site.register(DisplayPasta)
admin.site.register(DisplaySalad)
admin.site.register(DisplayTopping)
