from django.db import models
from django.utils.safestring import mark_safe


# Create your models here.

class Country(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=250)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


class ProductCategory(models.Model):
    name = models.CharField(verbose_name='Категория', max_length=25)
    anchor = models.CharField(verbose_name='Якорь для меню', max_length=10, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Наименование', max_length=250)
    price = models.DecimalField(verbose_name='Цена', max_digits=8, decimal_places=2)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL)
    unit_product = models.ForeignKey('UnitsProduct', on_delete=models.CASCADE)
    sale = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Картинка', upload_to='product')
    alt = models.CharField(verbose_name='Alt', max_length=250, null=True, blank=True)

    def pre_image(self):
        return mark_safe(f'<img src="{self.image.url}" width="100" height="100" />')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.alt is None:
            self.alt = self.image.name
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    def __str__(self):
        return f'{self.product.name} {self.image.url}'

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'

class UnitsProduct(models.Model):
    name = models.CharField(verbose_name='Единица товара', max_length=25)
    packaging = models.CharField(verbose_name='Упаковка', default='1', max_length=25)

    def __str__(self):
        return f'{self.name} - {self.packaging}'

    class Meta:
        verbose_name = 'Единица товара'
        verbose_name_plural = 'Единицы товара'