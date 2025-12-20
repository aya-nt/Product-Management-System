from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # Root URL redirect to product list
    path('', RedirectView.as_view(url='/list_produits/', permanent=False), name='home'),
    path('commandes/delete/<int:commande_id>/', views.delete_commande, name='delete_commande'),
    # Product URLs
    path('list_produits/', views.afficher_produits, name='list_produits'),
    path('search_product/', views.rechercher_produits, name='search_product'),
    
    # Order (Commande) URLs
    path('commander/', views.commander_prd, name='commander'),
    path('commandes/', views.afficher_cmd, name='CmdList'),
    path('commandes/edit/<int:pk>/', views.edit_cmd, name='CmdEdit'),
    path('commandes/delete/<int:pk>/', views.delete_cmd, name='CmdDelete'),
]
