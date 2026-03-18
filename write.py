import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def save_products(filename, products):
    """
    Saves the list of products to a specified file in CSV format.

    Each product is written as a comma-separated line containing:
    - Product Name
    - Brand
    - Quantity
    - Cost Price (rounded to two decimal places)
    - Country

    This function overwrites the file if it already exists.

    Parameters:
    filename (str): The name of the file to write the product data to.
    products (list): A list of dictionaries, each representing a product.

    Returns:
    bool: True if saving was successful, False otherwise.
    """
    
    try:
        filepath = os.path.join(BASE_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            for p in products:
                line = f"{p['Name of product']},{p['Brand']},{p['Quantity']},{p['Cost Price']:.2f},{p['Country']}\n"
                f.write(line)
        return True
    except Exception as e:
        print(f"Error saving products: {str(e)}")
        return False

def generate_invoice(transaction_type, product, quantity, vendor_name, customer_name=None, amount=None, vat_rate=0.15):
    """
    Generates a text-based invoice file for either a sale or a restock transaction.

    The function creates a uniquely named invoice file (with a timestamp)
    containing all relevant transaction details such as product name, brand,
    quantity, unit price/cost, VAT calculation, and total amount.

    For sales:
    - Requires customer name and amount (total before VAT).
    - Applies a "buy 3 get 1 free" promotion.
    - Calculates VAT and final total, and includes it in the invoice.

    For restocking:
    - Calculates total restocking cost including VAT.
    - Shows previous and updated stock levels.
    
    Parameters:
    transaction_type (str): Type of transaction, either "sale" or "restock".
    product (dict): A dictionary containing product details.
    quantity (int): Quantity of product sold or restocked.
    vendor_name (str): The name of the vendor or supplier.
    customer_name (str, optional): The name of the customer (required for sales).
    amount (float, optional): The subtotal amount for the sale (required for sales).
    vat_rate (float): VAT rate as a decimal (default is 0.15 for 15%).

    Returns:
    bool: True if invoice was successfully generated, False otherwise.
    """
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    prefix = "sale" if transaction_type == "sale" else "restock"
    filename = os.path.join(BASE_DIR, f"{prefix}_invoice_{timestamp}.txt")
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            if transaction_type == "sale":
                # Validate required fields for sales
                if customer_name is None or amount is None:
                    raise ValueError("Customer name and amount are required for sales")
                
                # Calculate VAT and totals
                subtotal = round(amount, 2)
                vat_amount = round(subtotal * vat_rate, 2)
                total_with_vat = round(subtotal + vat_amount, 2)
                free_items = quantity // 3 if quantity >= 3 else 0
                
                # Write sale invoice
                f.write("======= PRODUCT SALE INVOICE =======\n")
                f.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Vendor  : {vendor_name}\n")
                f.write(f"Customer: {customer_name}\n")
                f.write("------------------------------------\n")
                f.write(f"Product Name  : {product['Name of product']}\n")
                f.write(f"Brand         : {product['Brand']}\n")
                f.write(f"Country       : {product['Country']}\n")
                f.write(f"Unit Price    : {product['Selling Price']:.2f}\n")
                f.write(f"Quantity Sold : {quantity}\n")
                if free_items > 0:
                    f.write(f"Free Items    : {free_items} (buy 3 get 1 free)\n")
                f.write("------------------------------------\n")
                f.write(f"Subtotal      : {subtotal:.2f}\n")
                f.write(f"VAT ({vat_rate*100:.0f}%)      : {vat_amount:.2f}\n")
                f.write(f"Total Amount  : {total_with_vat:.2f}\n")
                f.write("====================================\n")
                f.write("Thank you for your purchase!\n")
                f.write("====================================\n")
                
          
            elif transaction_type == "restock":
                # Sanity check
                if not isinstance(product['Quantity'], (int, float)):
                    raise TypeError("Product 'Quantity' must be a number")

                # Calculate costs with VAT
                unit_cost = round(product['Cost Price'], 2)
                subtotal = round(quantity * unit_cost, 2)
                vat_amount = round(subtotal * vat_rate, 2)
                total_with_vat = round(subtotal + vat_amount, 2)
                new_stock = product['Quantity'] + quantity

                # Write restock invoice
                f.write("======= RESTOCK INVOICE =======\n")
                f.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Vendor  : {vendor_name}\n")
                f.write("------------------------------------\n")
                f.write(f"Product Name  : {product['Name of product']}\n")
                f.write(f"Brand         : {product['Brand']}\n")
                f.write(f"Country       : {product['Country']}\n")
                f.write(f"Unit Cost     : {unit_cost:.2f}\n")
                f.write(f"Quantity Added: {quantity}\n")
                f.write(f"Previous Stock: {product['Quantity']}\n")
                f.write(f"New Stock Level: {new_stock}\n")
                f.write("------------------------------------\n")
                f.write(f"Subtotal      : {subtotal:.2f}\n")
                f.write(f"VAT ({vat_rate*100:.0f}%)      : {vat_amount:.2f}\n")
                f.write(f"Total Cost    : {total_with_vat:.2f}\n")
                f.write("================================\n")
                f.write("Restock completed successfully!\n")
                f.write("================================\n")

            else:
                raise ValueError("Invalid transaction type. Use 'sale' or 'restock'")
               
        print(f"Invoice successfully generated: {filename}")
        return True
        
    except Exception as e:
        print(f"Error generating invoice: {str(e)}")
        return False