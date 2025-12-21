from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from .models import Product, Commande
from .forms import CommandeForm
import os
from supabase import create_client, Client

# Initialize Supabase client safely
def get_supabase_client():
    """Get Supabase client, return None if credentials are missing"""
    supabase_url = os.environ.get("VITE_SUPABASE_URL") or os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("VITE_SUPABASE_ANON_KEY") or os.environ.get("SUPABASE_ANON_KEY")
    
    if not supabase_url or not supabase_key:
        return None
    
    try:
        return create_client(supabase_url, supabase_key)
    except Exception as e:
        print(f"Error creating Supabase client: {e}")
        return None

supabase = get_supabase_client()

@require_http_methods(["POST"])

def delete_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    commande.delete()
    messages.success(request, 'La commande a été supprimée avec succès.')
    return redirect('CmdList')


def afficher_produits(request):
    """
    Display all products in the database.
    URL: /list_produits/
    """
    if not supabase:
        messages.error(request, "Configuration Supabase manquante")
        return render(request, "index.html", {"products": []})
    
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
    if not supabase:
        return render(request, 'search.html', {'error': 'Configuration Supabase manquante'})
    
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
    if not supabase:
        messages.error(request, "Configuration Supabase manquante")
        return render(request, 'commande.html', {
            'form': CommandeForm(),
            'products': []
        })
    
    # Fetch products from Supabase
    try:
        response = supabase.table("products").select("*").execute()
        products = response.data
    except Exception as e:
        print(f"ERROR fetching products from Supabase: {str(e)}")
        products = []
        messages.error(request, "Erreur lors du chargement des produits. Veuillez réessayer plus tard.")

    if request.method == 'POST':
        form = CommandeForm(request.POST)
        
        if form.is_valid():
            try:
                product_id = request.POST.get('Produit_cmd')
                if not product_id:
                    raise ValidationError("Veuillez sélectionner un produit")
                
                if not supabase:
                    raise Exception("Configuration Supabase manquante")
                
                # Get the selected product from Supabase
                response = supabase.table("products").select("*").eq("id", product_id).execute()
                if not response.data:
                    raise Exception("Produit sélectionné non trouvé")
                
                product_data = response.data[0]
                
                # Create or update the local Product instance
                product, created = Product.objects.update_or_create(
                    id=product_data['id'],
                    defaults={
                        'prd_name': product_data['name'],
                        'prd_price': product_data['price'],
                        'prd_ingredients': product_data.get('ingredients', '')
                    }
                )
                
                # Create the order
                commande = Commande(
                    Description_cmd=form.cleaned_data['Description_cmd'],
                    Date_cmd=form.cleaned_data['Date_cmd'],
                    Produit_cmd=product
                )
                commande.save()
                
                messages.success(request, 'Commande envoyée avec succès!')
                return redirect('CmdList')
                
            except Exception as e:
                print(f"Error creating order: {e}")
                messages.error(request, f"Erreur lors de l'envoi de la commande: {str(e)}")
    else:
        form = CommandeForm()

    return render(request, 'commande.html', {
        'form': form,
        'products': products
    })
            

def afficher_cmd(request):
    """
    Display all orders (commandes).
    URL: /commandes/
    """
    # Get all orders from the database
    commandes = Commande.objects.select_related('Produit_cmd').all().order_by('-Date_cmd')
    
    return render(request, 'CmdList.html', {'commandes': commandes})


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
