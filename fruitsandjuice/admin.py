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


class CartsInline(admin.TabularInline):
    model = OrderItem
    can_delete = True
    fields = ('product', 'unit_product_admin', 'price_admin',)
    readonly_fields = ('unit_product_admin', 'price_admin',)

    def unit_product_admin(self, obj):
        return obj.product.unit_product

    def price_admin(self, obj):
        return obj.product.price

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
    list_display = ('pk',
                    'user_name',
                    'mobile',
                    'payment_method',
                    'adress',
                    'status',
                    'delivery_method')
    inlines = [CartsInline, ]


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product')


admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImages, ProductImagesAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(UnitsProduct, UnitsProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
