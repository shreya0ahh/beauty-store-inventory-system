import os

def load_products(filename):
    '''
    Reads product information from a given text file and returns a list of product dictionaries.

    Each line in the file is expected to be in the format:
    Product Name, Brand, Quantity, Cost Price, Country

    The function processes each line, calculates the selling price (200% markup),
    and stores the data as a dictionary with the following keys:
    - 'Name of product'
    - 'Brand'
    - 'Quantity'
    - 'Cost Price'
    - 'Selling Price'
    - 'Country'

    Malformed lines are skipped with an error message.
    If the file is not found, a warning is printed and an empty list is returned.

    Parameters:
    filename (str): The name of the file containing product data.

    Returns:
    list: A list of dictionaries, each representing a product.
    '''
    products = []
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    parts = line.strip().split(',')
                    if len(parts) >= 5:
                        name = parts[0].strip()
                        brand = parts[1].strip()
                        quantity = parts[2].strip()
                        cost_price = parts[3].strip()
                        country = parts[4].strip()

                        product = {
                            'Name of product': name,
                            'Brand': brand,
                            'Quantity': int(quantity),
                            'Cost Price': round(float(cost_price), 2),
                            'Selling Price': round(float(cost_price) * 2, 2),
                            'Country': country
                        }
                        products.append(product)
                except ValueError as e:
                    print(f"Skipping malformed line: {line.strip()} (Error: {str(e)})")
    except FileNotFoundError:
        print(f"Warning: File not found - {filename}. Starting with empty product list.")
    return products