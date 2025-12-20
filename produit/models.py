import uuid
from django.db import models
from django.utils import timezone


class Product(models.Model):
    """
    Model representing a product in the database.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prd_name = models.CharField(max_length=100, verbose_name="Nom du produit")
    prd_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    prd_ingredients = models.TextField(verbose_name="Ingrédients", blank=True)
    
    def __str__(self):
        return self.prd_name
    
    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"


class Commande(models.Model):
    """
    Model representing an order (commande) in the database.
    """
    Description_cmd = models.CharField(max_length=200, verbose_name="Description")
    Date_cmd = models.DateField(default=timezone.now, verbose_name="Date de commande")
    Produit_cmd = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        verbose_name="Produit"
    )
    
    def __str__(self):
        return self.Description_cmd
    
    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ['-Date_cmd']  # Most recent first
