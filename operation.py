"""
operation.py - Handles core product operations for WeCare Beauty Store.

This module includes functions to:
- Display the current inventory in a formatted table.
- Validate user inputs for sales and restocking.
- Process product sales, updating stock and generating invoices.
- Process product restocking, allowing cost updates and invoice generation.
"""

from write import generate_invoice

def display_products(products):
     """
    Displays the list of products in a formatted table.

    Parameters:
        products (list): A list of dictionaries representing product data.
    
    Returns:
        None
    """
     print("\nAvailable Products:")
     print("=" * 80)
     print(f"{'No.':<4} {'Product':<35} {'Price':<10} {'Stock':<8} {'Country'}")
     print("-" * 80)
     for i, p in enumerate(products, 1):
        product_name = f"{p['Name of product']} ({p['Brand']})"
        price = f"{p['Selling Price']:.2f}"
        print(f"{i:<4} {product_name:<35} {price:<10} {p['Quantity']:<8} {p['Country']}")
     print("=" * 80)

def validate_inputs(product_name, quantity, vendor_name, customer_name=None, new_cost=None):
    """
    Validates and sanitizes inputs for sale or restock operations.

    Parameters:
        product_name (str): Name of the product.
        quantity (int): Quantity to sell or restock.
        vendor_name (str): Name of the vendor or supplier.
        customer_name (str, optional): Name of the customer (for sales only).
        new_cost (float, optional): New cost price (for restocking only).

    Returns:
        dict: Sanitized and validated input values.

    Raises:
        ValueError: If any of the inputs are invalid (e.g., non-numeric quantity,
                    empty or numeric customer/vendor names, invalid price).
    """
    # Validate product name
    if not isinstance(product_name, str) or not product_name.strip():
        raise ValueError("Product name cannot be empty")
    
    # Validate quantity
    try:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer")
    except ValueError:
        raise ValueError("Quantity must be a whole number")
    
    # Validate vendor name
    if not isinstance(vendor_name, str) or not vendor_name.strip():
        raise ValueError("Vendor name cannot be empty")
    if any(char.isdigit() for char in vendor_name):
        raise ValueError("Vendor name cannot contain numbers")
    
    # Validate customer name (if provided)
    if customer_name is not None:
        if not isinstance(customer_name, str) or not customer_name.strip():
            raise ValueError("Customer name cannot be empty")
        if any(char.isdigit() for char in customer_name.strip()):
            raise ValueError("Customer name cannot contain any digits")
        if customer_name.strip().isdigit():
            raise ValueError("Customer name cannot be purely numeric")
    
    # Validate new cost (if provided)
    if new_cost is not None:
        try:
            new_cost = float(new_cost)
            if new_cost <= 0:
                raise ValueError("Cost must be a positive number")
        except ValueError:
            raise ValueError("Cost must be a valid number")
    
    return {
        'product_name': product_name.strip(),
        'quantity': quantity,
        'vendor_name': vendor_name.strip(),
        'customer_name': customer_name.strip() if customer_name else None,
        'new_cost': round(float(new_cost), 2) if new_cost is not None else None
    }

def sell_product(products, product_name, quantity, vendor_name, customer_name):
    """
    Processes a sale by reducing stock, validating inputs, and generating an invoice.

    Parameters:
        products (list): List of current product dictionaries.
        product_name (str): Name of the product being sold.
        quantity (int): Number of units being sold.
        vendor_name (str): Name of the vendor/store.
        customer_name (str): Name of the customer.

    Returns:
        bool: True if the sale is successful, False otherwise.
    """

    try:
        validated = validate_inputs(product_name, quantity, vendor_name, customer_name)
    except ValueError as e:
        if "Customer name cannot contain any digits" in str(e) or "Customer name cannot be purely numeric" in str(e):
            print(f"ALERT: Invalid customer name '{customer_name}'. Names cannot contain digits or be purely numeric.")
        else:
            print(f"Error: {e}")
        return False

    for product in products:
        if product['Name of product'].lower() == validated['product_name'].lower():
            if product['Quantity'] >= validated['quantity']:
                product['Quantity'] -= validated['quantity']
                total_price = round(validated['quantity'] * product['Selling Price'], 2)
                print(f"\nSold {validated['quantity']} units of {product['Name of product']}. Total: ${total_price:.2f}")
                
                generate_invoice(
                    transaction_type="sale",
                    product=product,
                    quantity=validated['quantity'],
                    vendor_name=validated['vendor_name'],
                    customer_name=validated['customer_name'],
                    amount=total_price
                )
                return True
            else:
                print("Not enough stock available.")
                return False
    print("Product not found.")
    return False

def restock_product(products, product_name, quantity, vendor_name, new_cost=None):
    """
    Processes restocking of a product, including quantity update and optional price adjustment.

    Parameters:
        products (list): List of current product dictionaries.
        product_name (str): Name of the product to restock.
        quantity (int): Number of units to add.
        vendor_name (str): Name of the supplier.
        new_cost (float, optional): New cost price to update, if provided.

    Returns:
        bool: True if restocking was successful, False otherwise.
    """
    try:
        validated = validate_inputs(product_name, quantity, vendor_name, new_cost=new_cost)
    except ValueError as e:
        print(f"Error: {e}")
        return False

    for product in products:
        if product['Name of product'].lower() == validated['product_name'].lower():
            product['Quantity'] += validated['quantity']
            
            if validated['new_cost'] and validated['new_cost'] > 0:
                product['Cost Price'] = validated['new_cost']
                product['Selling Price'] = round(validated['new_cost'] * 2, 2)
            
            print(f"Restocked {validated['quantity']} units of {product['Name of product']}. New quantity: {product['Quantity']}")
            
            generate_invoice(
                transaction_type="restock",
                product=product,
                quantity=validated['quantity'],
                vendor_name=validated['vendor_name']
            )
             
            return True
    print("Product not found.")
    return False