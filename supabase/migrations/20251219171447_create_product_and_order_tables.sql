/*
  # Product Management System Database Schema

  ## Overview
  Creates a simple database for managing products and orders (commandes) as described in the Django project.

  ## New Tables
  
  ### `products`
  - `id` (uuid, primary key) - Unique product identifier
  - `name` (text, required) - Product name
  - `ingredients` (text) - Product ingredients for search functionality
  - `description` (text) - Product description
  - `price` (decimal) - Product price
  - `created_at` (timestamptz) - Record creation timestamp
  - `updated_at` (timestamptz) - Record update timestamp
  
  ### `commandes` (orders)
  - `id` (uuid, primary key) - Unique order identifier
  - `product_id` (uuid, foreign key) - Reference to products table
  - `quantity` (integer) - Order quantity
  - `customer_name` (text, required) - Customer name
  - `customer_email` (text) - Customer email
  - `status` (text) - Order status (pending, completed, cancelled)
  - `total_price` (decimal) - Total order price
  - `created_at` (timestamptz) - Order creation timestamp
  - `updated_at` (timestamptz) - Order update timestamp

  ## Security
  - Enable Row Level Security (RLS) on both tables
  - Add policies for public read access (for product listing)
  - Add policies for authenticated users to manage orders
*/

-- Create products table
CREATE TABLE IF NOT EXISTS products (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  ingredients text DEFAULT '',
  description text DEFAULT '',
  price decimal(10, 2) NOT NULL DEFAULT 0,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create commandes (orders) table
CREATE TABLE IF NOT EXISTS commandes (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id uuid REFERENCES products(id) ON DELETE CASCADE,
  quantity integer NOT NULL DEFAULT 1,
  customer_name text NOT NULL,
  customer_email text DEFAULT '',
  status text DEFAULT 'pending',
  total_price decimal(10, 2) NOT NULL DEFAULT 0,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_products_name ON products(name);
CREATE INDEX IF NOT EXISTS idx_products_ingredients ON products(ingredients);
CREATE INDEX IF NOT EXISTS idx_commandes_product_id ON commandes(product_id);
CREATE INDEX IF NOT EXISTS idx_commandes_status ON commandes(status);

-- Enable Row Level Security
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE commandes ENABLE ROW LEVEL SECURITY;

-- Products policies: Allow public read access
CREATE POLICY "Anyone can view products"
  ON products FOR SELECT
  USING (true);

CREATE POLICY "Authenticated users can insert products"
  ON products FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Authenticated users can update products"
  ON products FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Authenticated users can delete products"
  ON products FOR DELETE
  TO authenticated
  USING (true);

-- Commandes policies: Allow public to create orders, authenticated users to manage
CREATE POLICY "Anyone can create orders"
  ON commandes FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Anyone can view orders"
  ON commandes FOR SELECT
  USING (true);

CREATE POLICY "Authenticated users can update orders"
  ON commandes FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Authenticated users can delete orders"
  ON commandes FOR DELETE
  TO authenticated
  USING (true);

-- Insert sample products
INSERT INTO products (name, ingredients, description, price) VALUES
  ('Chocolate Cake', 'flour, sugar, cocoa, eggs, butter', 'Delicious chocolate cake with rich cocoa flavor', 25.99),
  ('Vanilla Cupcakes', 'flour, sugar, vanilla, eggs, butter, milk', 'Light and fluffy vanilla cupcakes', 15.50),
  ('Strawberry Tart', 'flour, butter, sugar, strawberries, cream', 'Fresh strawberry tart with sweet cream', 18.75),
  ('Lemon Pie', 'flour, butter, lemons, sugar, eggs', 'Tangy lemon pie with buttery crust', 22.00),
  ('Blueberry Muffins', 'flour, blueberries, sugar, eggs, butter', 'Homemade blueberry muffins', 12.50)
ON CONFLICT DO NOTHING;