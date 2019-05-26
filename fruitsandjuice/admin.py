from django.contrib import admin


from fruitsandjuice.models import (
    ProductCategory,
    Product,
    ProductImages,
    Country,
    UnitsProduct, Order, OrderItem)


class ProductCategoryAdmin(admin.ModelAdmin):
    pass


class ImagesInline(admin.TabularInline):
    model = ProductImages
    readonly_fields = ('pre_image',)
    can_delete = True

    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra


class ProductAdmin(admin.ModelAdmin):
    inlines = [ImagesInline]


class ProductImagesAdmin(admin.ModelAdmin):
    pass


class CountryAdmin(admin.ModelAdmin):
    pass

class UnitsProductAdmin(admin.ModelAdmin):
    pass

class OrderAdmin(admin.ModelAdmin):
    pass

class OrderItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImages, ProductImagesAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(UnitsProduct, UnitsProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
