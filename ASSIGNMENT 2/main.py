from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 50, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 899, "category": "Electronics", "in_stock": True},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": False},
    {"id": 5, "name": "Bluetooth Speaker", "price": 1999, "category": "Electronics", "in_stock": True},
    {"id": 6, "name": "Sketchbook", "price": 199, "category": "Stationery", "in_stock": True},
    {"id": 7, "name": "Laptop Stand", "price": 1299, "category": "Electronics", "in_stock": False}
]

feedback = []
orders = []

@app.get("/")
def home():
    return {"message": "Welcome to our app"}
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
def get_in_stock_products():

    in_stock_products = []

    for product in products:
        if product["in_stock"] == True:
            in_stock_products.append(product)

    return {
        "in_stock_products": in_stock_products,
        "count": len(in_stock_products)
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

@app.get("/products/filter")
def filter_products(category: str = None, min_price: int = None, max_price: int = None):

    results = []

    for product in products:

        if category and product["category"].lower() != category.lower():
            continue

        if min_price and product["price"] < min_price:
            continue

        if max_price and product["price"] > max_price:
            continue

        results.append(product)

    return {
        "products": results,
        "count": len(results)
    }

@app.get("/products/{product_id}/price")
def get_product_price(product_id: int):

    for product in products:
        if product["id"] == product_id:
            return {
                "name": product["name"],
                "price": product["price"]
            }

    return {"error": "Product not found"}

# Creating pydantic model for feedback
class CustomerFeedback(BaseModel):
    customer_name: str = Field(..., min_length=2)
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=300)

@app.post("/feedback")
def submit_feedback(data: CustomerFeedback):

    feedback.append(data.dict())

    return {
        "message": "Feedback submitted successfully",
        "feedback": data,
        "total_feedback": len(feedback)
    }

@app.get("/products/summary")
def products_summary():

    total_products = len(products)

    in_stock_count = 0
    out_of_stock_count = 0
    categories = []

    cheapest = products[0]
    most_expensive = products[0]

    for product in products:

        # stock count
        if product["in_stock"]:
            in_stock_count += 1
        else:
            out_of_stock_count += 1

        # category list
        if product["category"] not in categories:
            categories.append(product["category"])

        # cheapest product
        if product["price"] < cheapest["price"]:
            cheapest = product

        # most expensive product
        if product["price"] > most_expensive["price"]:
            most_expensive = product

    return {
        "total_products": total_products,
        "in_stock_count": in_stock_count,
        "out_of_stock_count": out_of_stock_count,
        "most_expensive": {
            "name": most_expensive["name"],
            "price": most_expensive["price"]
        },
        "cheapest": {
            "name": cheapest["name"],
            "price": cheapest["price"]
        },
        "categories": categories
    }

class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=1, le=50)

from typing import List

class BulkOrder(BaseModel):
    company_name: str = Field(..., min_length=2)
    contact_email: str = Field(..., min_length=5)
    items: List[OrderItem] = Field(..., min_items=1)

# Creating post endpoint for bulk order
@app.post("/orders/bulk")
def place_bulk_order(order: BulkOrder):

    confirmed = []
    failed = []
    grand_total = 0

    for item in order.items:

        product_found = None

        # find product
        for product in products:
            if product["id"] == item.product_id:
                product_found = product
                break

        # product not found
        if not product_found:
            failed.append({
                "product_id": item.product_id,
                "reason": "Product not found"
            })
            continue

        # check stock
        if not product_found["in_stock"]:
            failed.append({
                "product_id": item.product_id,
                "reason": f'{product_found["name"]} is out of stock'
            })
            continue

        # calculate subtotal
        subtotal = product_found["price"] * item.quantity
        grand_total += subtotal

        confirmed.append({
            "product": product_found["name"],
            "qty": item.quantity,
            "subtotal": subtotal
        })

    return {
        "company": order.company_name,
        "confirmed": confirmed,
        "failed": failed,
        "grand_total": grand_total
    }

# post- create order endpoint
@app.post("/orders")
def create_order(order: BulkOrder):

    order_id = len(orders) + 1

    new_order = {
        "order_id": order_id,
        "company": order.company_name,
        "contact_email": order.contact_email,
        "items": [item.dict() for item in order.items],
        "status": "pending"
    }

    orders.append(new_order)

    return new_order

# Get order by id
@app.get("/orders/{order_id}")
def get_order(order_id: int):

    for order in orders:
        if order["order_id"] == order_id:
            return order

    return {"error": "Order not found"}

# Confirm order
@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id: int):

    for order in orders:
        if order["order_id"] == order_id:

            order["status"] = "confirmed"
            return {
                "message": "Order confirmed",
                "order": order
            }

    return {"error": "Order not found"}