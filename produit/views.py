from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, Commande
from .forms import CommandeForm
import os
from supabase import create_client, Client

supabase: Client = create_client(
    os.environ.get("VITE_SUPABASE_URL"),
    os.environ.get("VITE_SUPABASE_ANON_KEY") or os.environ.get("VITE_SUPABASE_SUPABASE_ANON_KEY")
)


def afficher_produits(request):
    """
    Display all products in the database.
    URL: /list_produits/
    """
    try:
        response = supabase.table("products").select("*").execute()
        produits = response.data
        print(f"DEBUG: Fetched {len(produits)} products from Supabase")
        formatted_products = [
            {
                "prd_name": p["name"],
                "prd_price": p["price"],
                "prd_ingredients": p["ingredients"]
            }
            for p in produits
        ]
        return render(request, "index.html", {"products": formatted_products})
    except Exception as e:
        import traceback
        print(f"Error fetching products: {e}")
        traceback.print_exc()
        return render(request, "index.html", {"products": []})


def rechercher_produits(request):
    """
    Search for products by name or ingredients (2-level search).
    URL: /search_product/
    """
    if request.method == "GET":
        query = request.GET.get('search', '').strip()

        if query:
            try:
                all_products = supabase.table("products").select("*").execute().data

                produits = [
                    {
                        "prd_name": p["name"],
                        "prd_price": p["price"],
                        "prd_ingredients": p["ingredients"]
                    }
                    for p in all_products
                    if query.lower() in p["name"].lower()
                ]

                if produits:
                    return render(request, 'search.html', {
                        'products': produits,
                        'query': query,
                        'search_level': 1
                    })
                else:
                    produits_ingredients = [
                        {
                            "prd_name": p["name"],
                            "prd_price": p["price"],
                            "prd_ingredients": p["ingredients"]
                        }
                        for p in all_products
                        if query.lower() in p["ingredients"].lower()
                    ]

                    return render(request, 'search.html', {
                        'products': produits_ingredients,
                        'query': query,
                        'search_level': 2,
                        'no_level1_results': True
                    })
            except Exception as e:
                print(f"Error searching products: {e}")
                return render(request, 'search.html', {'query': query})

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
