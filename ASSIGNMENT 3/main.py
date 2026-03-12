from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 50, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": False},
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

# -----------------------------
# Inventory audit endpoint
# -----------------------------

@app.get("/products/audit")
def products_audit():

    total_products = len(products)   # total number of products

    in_stock_count = 0               # count of products available
    out_of_stock_names = []          # list to store names of out-of-stock products

    total_stock_value = 0            # total inventory value (price * 10)

    most_expensive = products[0]     # assume first product is most expensive initially

    for product in products:

        # check stock status
        if product["in_stock"]:
            in_stock_count += 1

            # calculate stock value (assuming 10 units each)
            total_stock_value += product["price"] * 10

        else:
            out_of_stock_names.append(product["name"])

        # check most expensive product
        if product["price"] > most_expensive["price"]:
            most_expensive = product

    return {
        "total_products": total_products,
        "in_stock_count": in_stock_count,
        "out_of_stock_names": out_of_stock_names,
        "total_stock_value": total_stock_value,
        "most_expensive": {
            "name": most_expensive["name"],
            "price": most_expensive["price"]
        }
    }

# -----------------------------
# Apply discount to a category
# -----------------------------

@app.put("/products/discount")
def apply_discount(category: str, discount_percent: int):

    updated_products = []   # store updated products

    # check discount range (1–99)
    if discount_percent < 1 or discount_percent > 99:
        return {"error": "discount_percent must be between 1 and 99"}

    # loop through all products
    for product in products:

        # check category match
        if product["category"].lower() == category.lower():

            # apply discount formula
            new_price = int(product["price"] * (1 - discount_percent / 100))

            # update price
            product["price"] = new_price

            # store updated product info
            updated_products.append({
                "name": product["name"],
                "new_price": new_price
            })

    # if no products found
    if len(updated_products) == 0:
        return {"message": "No products found in this category"}

    return {
        "updated_count": len(updated_products),
        "updated_products": updated_products
    }


# -----------------------------
# GET single product by ID
# -----------------------------

@app.get("/products/{product_id}")
def get_product_by_id(product_id: int):

    # search product in list
    for product in products:
        if product["id"] == product_id:
            return product

    # if product not found
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Product not found")

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

# -----------------------------
# -----------------------------
# NEW CODE FOR DAY 4
# POST endpoint to add product
# -----------------------------

# Pydantic model for product input validation
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2)
    price: int = Field(..., gt=0)
    category: str
    in_stock: bool


# POST endpoint to add a product
@app.post("/products", status_code=201)
def add_product(product: ProductCreate):

    # Step 1: check if product name already exists
    for p in products:
        if p["name"].lower() == product.name.lower():
            # if duplicate → return 400 Bad Request
            raise HTTPException(status_code=400, detail="Product already exists")

    # Step 2: auto-generate ID
    new_id = len(products) + 1

    # Step 3: create product dictionary
    new_product = {
        "id": new_id,
        "name": product.name,
        "price": product.price,
        "category": product.category,
        "in_stock": product.in_stock
    }

    # Step 4: add product to list
    products.append(new_product)

    # Step 5: return success response
    return {
        "message": "Product added",
        "product": new_product
    }

# -----------------------------
# PUT endpoint to update product
# -----------------------------

@app.put("/products/{product_id}")
def update_product(product_id: int, price: int = None, in_stock: bool = None):

    # loop through products to find the product with given ID
    for product in products:

        if product["id"] == product_id:

            # update price if provided
            if price is not None:
                product["price"] = price

            # update stock if provided
            if in_stock is not None:
                product["in_stock"] = in_stock

            # return updated product
            return {
                "message": "Product updated",
                "product": product
            }

    # if product ID not found
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Product not found")

# -----------------------------
# DELETE endpoint to remove a product
# -----------------------------

from fastapi import HTTPException

@app.delete("/products/{product_id}")
def delete_product(product_id: int):

    # loop through the product list
    for product in products:

        # check if product ID matches
        if product["id"] == product_id:

            product_name = product["name"]   # store product name for response

            products.remove(product)         # remove product from list

            return {
                "message": f"Product '{product_name}' deleted"
            }

    # if product not found
    raise HTTPException(status_code=404, detail="Product not found")