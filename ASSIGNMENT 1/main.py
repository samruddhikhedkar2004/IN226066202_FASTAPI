from fastapi import FastAPI

app = FastAPI()

# Product list
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 599, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Bluetooth Speaker", "price": 1299, "category": "Electronics", "in_stock": True},
    {"id": 3, "name": "USB-C Cable", "price": 299, "category": "Accessories", "in_stock": True},
    {"id": 4, "name": "Laptop Bag", "price": 999, "category": "Accessories", "in_stock": False},

    # New products added
    {"id": 5, "name": "Laptop Stand", "price": 899, "category": "Accessories", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 1499, "category": "Electronics", "in_stock": True},
    {"id": 3, "name": "Notebook", "price": 50, "category": "Stationery", "in_stock": True},
    {"id": 4, "name": "Pen Set", "price": 120, "category": "Stationery", "in_stock": True},
]

@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }

# NEW ENDPOINT
@app.get("/products/category/{category_name}")
def get_products_by_category(category_name: str):
    
    filtered_products = []

    for product in products:
        if product["category"].lower() == category_name.lower():
            filtered_products.append(product)

    if len(filtered_products) == 0:
        return {"error": "No products found in this category"}

    return {"products": filtered_products}

@app.get("/products/instock")
def get_instock_products():

    instock_products = []

    for product in products:
        if product["in_stock"] == True:
            instock_products.append(product)

    return {
        "in_stock_products": instock_products,
        "count": len(instock_products)
    }

@app.get("/store/summary")
def store_summary():

    total_products = len(products)

    in_stock_count = 0
    out_of_stock_count = 0
    categories = []

    for product in products:

        # count stock
        if product["in_stock"]:
            in_stock_count += 1
        else:
            out_of_stock_count += 1

        # collect unique categories
        if product["category"] not in categories:
            categories.append(product["category"])

    return {
        "store_name": "My E-commerce Store",
        "total_products": total_products,
        "in_stock": in_stock_count,
        "out_of_stock": out_of_stock_count,
        "categories": categories
    }

@app.get("/products/search/{keyword}")
def search_products(keyword: str):

    matched_products = []

    for product in products:
        if keyword.lower() in product["name"].lower():
            matched_products.append(product)

    if len(matched_products) == 0:
        return {"message": "No products matched your search"}

    return {
        "matched_products": matched_products,
        "total_matches": len(matched_products)
    }

@app.get("/products/deals")
def get_product_deals():

    cheapest_product = products[0]
    most_expensive_product = products[0]

    for product in products:

        if product["price"] < cheapest_product["price"]:
            cheapest_product = product

        if product["price"] > most_expensive_product["price"]:
            most_expensive_product = product

    return {
        "best_deal": cheapest_product,
        "premium_pick": most_expensive_product
    }