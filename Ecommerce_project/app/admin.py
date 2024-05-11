from django.contrib import admin
from .models import *

# Inline classes for ProductAdmin
class ProductImageInline(admin.TabularInline):
    model = ProductImage

class AdditionalInformationInline(admin.TabularInline):
    model = AdditionalInformation

class ProductAdmin(admin.ModelAdmin):
    # Adding inlines to ProductAdmin
    inlines = [ProductImageInline, AdditionalInformationInline]
    list_display = ('product_name','price','Categories','color','section')
    list_editable = ('Categories','section','color')

# Registering models with admin
admin.site.register(Slider)
admin.site.register(BannerArea)
admin.site.register(MainCategory)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Section)
admin.site.register(Product, ProductAdmin)  # Using ProductAdmin for Product model
admin.site.register(Color)
admin.site.register(BrandName)
