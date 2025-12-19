from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, Commande
from .forms import CommandeForm


def afficher_produits(request):
    """
    Display all products in the database.
    URL: /list_produits/
    """
    produits = Product.objects.all()
    return render(request, "index.html", {"products": produits})


def rechercher_produits(request):
    """
    Search for products by name or ingredients (2-level search).
    URL: /search_product/
    """
    if request.method == "GET":
        query = request.GET.get('search', '').strip()
        
        if query:
            # Level 1 search: Search by product name
            produits = Product.objects.filter(prd_name__icontains=query)
            
            if produits.exists():
                # Found products by name
                return render(request, 'search.html', {
                    'products': produits,
                    'query': query,
                    'search_level': 1
                })
            else:
                # Level 2 search: Search by ingredients
                produits_ingredients = Product.objects.filter(
                    prd_ingredients__icontains=query
                )
                
                return render(request, 'search.html', {
                    'products': produits_ingredients,
                    'query': query,
                    'search_level': 2,
                    'no_level1_results': True
                })
        
        return render(request, 'search.html')


def commander_prd(request):
    """
    Create a new order (commande).
    URL: /commander/
    """
    if request.method == 'POST':
        form = CommandeForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Commande envoyée avec succès!')
            return redirect('commander')
    else:
        form = CommandeForm()
    
    message = "Veuillez remplir tous les champs pour passer une commande."
    return render(request, "commande.html", {"form": form, "message": message})


def afficher_cmd(request):
    """
    Display all orders (commandes).
    URL: /commandes/
    """
    cmds = Commande.objects.all()
    return render(request, "CmdList.html", {"commandes": cmds})


def edit_cmd(request, pk):
    """
    Edit an existing order (commande).
    URL: /commandes/edit/<pk>/
    """
    cmd = get_object_or_404(Commande, id=pk)
    
    if request.method == 'POST':
        form = CommandeForm(request.POST, instance=cmd)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Commande modifiée avec succès!')
            return redirect("CmdList")
    else:
        form = CommandeForm(instance=cmd)
    
    return render(request, 'CmdEdit.html', {"form": form, "commande": cmd})


def delete_cmd(request, pk):
    """
    Delete an order (commande) with confirmation.
    URL: /commandes/delete/<pk>/
    """
    cmd = get_object_or_404(Commande, id=pk)
    
    if request.method == 'POST':
        cmd.delete()
        messages.success(request, 'Commande supprimée avec succès!')
        return redirect("CmdList")
    
    return render(request, 'CmdDelete.html', {"commande": cmd})
