from django.db import models

# Create your models here.
class Category(models.Model):
    class Meta:
        verbose_name = ('Категория')
        verbose_name_plural = ('Категории')

    def __str__(self):
        return self.name
    name = models.CharField(max_length=100)

class Product(models.Model):
    class Meta:
        verbose_name = ('Товар')
        verbose_name_plural = ('Товары')

    def __str__(self):
        return self.name
    
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)