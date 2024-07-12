def products_dict(products_arr):
    products = []
    for product in products_arr:
        shoe = {
            "name": product.product_name,
            "size": product.product_size,
            "color": product.product_color,
            "sold_price": product.product_sold_price,
            "get_price": product.product_get_price,
            "sold_time": product.product_sold_time,
        }
        products.append(shoe)
    
    return products