"""
WeCare Beauty Store Management System

This script provides an interactive command-line system for managing
inventory, processing sales with promotional logic, restocking products,
and generating VAT-inclusive invoices for a local beauty and skincare store.

Modules:
- read.py: Loads product data.
- operation.py: Handles display, sales, and restocking logic.
- write.py: Saves updated products and generates invoices.

Main Features:
- Display current inventory.
- Sell products with 'buy 3 get 1 free' logic.
- Restock existing or new products.
- Generate and save formatted invoices.
"""
import datetime
from read import load_products
from operation import display_products as op_display_products, sell_product, restock_product
from write import save_products, generate_invoice

def process_sale(products):
    """
    Handles the product sale process with user interaction.

    - Prompts for a valid customer name.
    - Allows the user to select products and specify quantities.
    - Applies 'buy 3 get 1 free' discount.
    - Ensures stock availability and updates quantities accordingly.
    - Generates individual invoices for each item in the cart.
    - Saves updated product list to the inventory file.

    Parameters:
        products (list): List of current product dictionaries.

    Returns:
        list: Updated product list after sale.
    """
    customer_name = input("Enter customer name: ")
    if customer_name.lower().strip("'\"") == 'done':
        print("Sale cancelled. Returning to main menu.")
        return products
        
    # Validate customer name before proceeding
    try:
        if any(char.isdigit() for char in customer_name.strip()) or customer_name.strip().isdigit():
            print(f"ALERT: Invalid customer name '{customer_name}'. Names cannot contain digits or be purely numeric.")
            print("Sale cancelled. Returning to main menu.")
            return products
    except AttributeError:
        print("ALERT: Customer name must be a valid string.")
        print("Sale cancelled. Returning to main menu.")
        return products

    cart = []
    total_amount = 0
    while True:
        op_display_products(products)
        choice = input("Enter product number to add to cart (or 'done' to finish): ").strip().lower().strip("'\"")
        
        if choice == 'done':
            if not cart:
                print("Sale cancelled. No items were added.")
                return products
            break
            
        try:
            product_idx = int(choice) - 1
            if 0 <= product_idx < len(products):
                product = products[product_idx]
                try:
                    quantity = int(input(f"How many {product['Name of product']} you want to buy? (Available: {product['Quantity']}): "))
                    if quantity <= 0:
                        print("Quantity must be positive.")
                        continue
                    
                    if quantity > product['Quantity']:
                        print(f"Not enough stock. Only {product['Quantity']} available.")
                        continue
                    
                    # Calculate maximum possible quantity with free items
                    max_with_free = 0
                    free_items = 0
                    
                    # Find maximum quantity where quantity + floor(quantity/3) <= available stock
                    for q in range(quantity, 0, -1):
                        potential_free = q // 3
                        if q + potential_free <= product['Quantity']:
                            max_with_free = q
                            free_items = potential_free
                            break
                    
                    if max_with_free == 0:
                        print("Cannot process this quantity with free items.")
                        continue
                        
                    if max_with_free < quantity:
                        print(f"Adjusted quantity from {quantity} to {max_with_free} to accommodate free items.")
                        quantity = max_with_free
                    
                    # Add to cart
                    cart.append({
                        'product': product,
                        'quantity': quantity,
                        'free_items': free_items,
                        'amount': quantity * product['Selling Price']
                    })
                    total_amount += quantity * product['Selling Price']
                    
                    # Update stock
                    product['Quantity'] -= (quantity + free_items)
                    
                    print(f"Added {quantity} {product['Name of product']} (+{free_items} free) to cart.")
                except ValueError:
                    print("Please enter a valid number.")
            else:
                print("Invalid product number.")
        except ValueError:
            print("Please enter a valid product number or 'done' to finish.")
    
    if not cart:
        print("No items in cart. Sale cancelled.")
        return products
    
    # Generate invoice for each item
    for item in cart:
        generate_invoice(
            transaction_type="sale",
            product=item['product'],
            quantity=item['quantity'],
            vendor_name="WeCare Store",
            customer_name=customer_name,
            amount=item['amount']
        )
    
    # Save updated inventory
    save_products("wecare_products.txt", products)
    
    print("\nSale completed successfully!")
    print(f"Total Amount: {total_amount:.2f}")
    return products

def process_restock(products):
    """
    Handles restocking of products, including adding new items.

    - Prompts for supplier name.
    - Displays current inventory.
    - Allows restocking existing items or adding new ones.
    - Updates quantities and optionally cost prices.
    - Generates restock invoices for each item added.
    - Saves updated inventory to file.

    Parameters:
        products (list): List of current product dictionaries.

    Returns:
        list: Updated product list after restocking.
    """
    supplier_name = input("Enter supplier name: ")
    if supplier_name.lower().strip("'\"") == 'done':
        print("Restocking cancelled. Returning to main menu.")
        return products
        
    restock_items = []
    total_cost = 0
    
    while True:
        op_display_products(products)
        print("0. Add new product")
        choice = input("Enter product number (or 'done' to finish): ").strip().lower().strip("'\"")
        
        if choice == 'done':
            if not restock_items:
                print("Restocking cancelled. No items were added.")
                return products
            break
            
        try:
            choice = int(choice)
            if choice == 0:
                name = input("Enter product name: ")
                brand = input("Enter brand: ")
                quantity = int(input("Enter quantity: "))
                cost_price = float(input("Enter cost price: "))
                country = input("Enter country of origin: ")
                
                new_product = {
                    'Name of product': name,
                    'Brand': brand,
                    'Quantity': quantity,
                    'Cost Price': round(cost_price, 2),
                    'Selling Price': round(cost_price * 2, 2),
                    'Country': country
                }
                
                products.append(new_product)
                restock_items.append({
                    'product': new_product,
                    'quantity': quantity,
                    'cost_price': cost_price,
                    'is_new': True
                })
                total_cost += quantity * cost_price
                print(f"Added new product: {name}")
            elif 1 <= choice <= len(products):
                product = products[choice-1]
                try:
                    quantity = int(input(f"How many {product['Name of product']} units to add? "))
                    if quantity <= 0:
                        print("Quantity must be positive.")
                        continue
                    
                    new_cost = input(f"Enter new cost price (or press Enter to keep {product['Cost Price']:.2f}): ")
                    if new_cost:
                        product['Cost Price'] = float(new_cost)
                        product['Selling Price'] = float(new_cost) * 2
                    
                    product['Quantity'] += quantity
                    restock_items.append({
                        'product': product,
                        'quantity': quantity,
                        'cost_price': product['Cost Price'],
                        'is_new': False
                    })
                    total_cost += quantity * product['Cost Price']
                    print(f"Added {quantity} {product['Name of product']} to inventory.")
                except ValueError:
                    print("Please enter a valid number.")
            else:
                print("Invalid product number.")
        except ValueError:
            print("Please enter a valid product number or 'done' to finish.")
    
    # Generate restock invoices
    for item in restock_items:
        generate_invoice(
            transaction_type="restock",
            product=item['product'],
            quantity=item['quantity'],
            vendor_name=supplier_name
        )
    
    save_products("wecare_products.txt", products)
    print("\nRestocking completed successfully!")
    print(f"Total Cost: {total_cost:.2f}")
    return products

def main():
     """
    Entry point of the WeCare Management System.

    - Loads product inventory from file.
    - Displays a menu for user interaction.
    - Allows users to display products, process sales, restock products, or exit.
    - Continuously prompts until the user chooses to exit.
    """
     print("Welcome to WeCare Beauty Store Management System")
     products = load_products("wecare_products.txt")
    
     while True:
        print("\nMain Menu:")
        print("1. Display Products")
        print("2. Process Sale")
        print("3. Process Restock")
        print("4. Exit")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            op_display_products(products)
        elif choice == '2':
            products = process_sale(products)
        elif choice == '3':
            products = process_restock(products)
        elif choice == '4':
            print("Thank you for using WeCare Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()