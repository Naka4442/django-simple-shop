from django.contrib import admin
from .models import Product, Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    fieldsets = (
        (('Основная информация'), {
            'fields': ('name', 'category', 'price')
        }),
        (('Дополнительно'), {
            'fields': ('description', 'image'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Русификация заголовка админки
admin.site.site_header = ('Администрирование магазина')
admin.site.site_title = ('Магазин')
admin.site.index_title = ('Панель управления')