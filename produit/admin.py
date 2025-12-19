from django.contrib import admin
from .models import Product, Commande


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for Product model.
    """
    list_display = ('prd_name', 'prd_price', 'prd_ingredients')
    search_fields = ('prd_name', 'prd_ingredients')
    list_filter = ('prd_price',)


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    """
    Admin configuration for Commande model.
    """
    list_display = ('Description_cmd', 'Date_cmd', 'Produit_cmd')
    search_fields = ('Description_cmd',)
    list_filter = ('Date_cmd', 'Produit_cmd')
    date_hierarchy = 'Date_cmd'
