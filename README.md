# Django Product Management System

A complete Django web application for managing products and orders (commandes) .

## Features

- **Product Listing**: Display all available products
- **Product Search**: Search products by name and ingredients (2-level search)
- **Order Management**: Create, view, edit, and delete orders
- **Bootstrap Integration**: Modern, responsive UI with Bootstrap 5

## Project Structure

```
project/
├── manage.py
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── produit/
    ├── __init__.py
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── forms.py
    ├── admin.py
    └── templates/
        ├── base.html
        ├── index.html
        ├── search.html
        ├── commande.html
        ├── CmdList.html
        └── CmdEdit.html
```

## URLs

| URL | Description |
|-----|-------------|
| `/list_produits/` | Display all products |
| `/search_product/` | Search for products |
| `/commander/` | Create a new order |
| `/commandes/` | View all orders |
| `/commandes/edit/<id>/` | Edit an order |
| `/commandes/delete/<id>/` | Delete an order |

## Technologies Used

- Django 4.x
- Bootstrap 5.2
- SQLite (default Django database)
