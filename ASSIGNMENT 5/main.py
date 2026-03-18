from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Pen set", "price": 49, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
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
# Sort products Assignment 5
# -----------------------------
@app.get("/products/sort")
def sort_products(sort_by: str = "price", order: str = "asc"):

    # Step 1: Validate sort_by
    if sort_by not in ["price", "name"]:
        return {"error": "sort_by must be 'price' or 'name'"}

    # Step 2: Validate order
    if order not in ["asc", "desc"]:
        return {"error": "order must be 'asc' or 'desc'"}

    # Step 3: Sort products
    reverse = True if order == "desc" else False

    sorted_products = sorted(products, key=lambda x: x[sort_by], reverse=reverse)

    return {
        "sort_by": sort_by,
        "order": order,
        "products": sorted_products
    }

# -----------------------------
# Pagination - view products page-wise
# -----------------------------
@app.get("/products/page")
def paginate_products(page: int = 1, limit: int = 2):

    if page  < 1 or limit < 1:
      return {"error": "page and limit must be greater than 0"}

    # Step 1: calculate total products
    total_products = len(products)

    # Step 2: calculate total pages
    total_pages = (total_products + limit - 1) // limit

    # Step 3: calculate start and end index
    start = (page - 1) * limit
    end = start + limit

    # Step 4: slice the products list
    paginated_products = products[start:end]

    return {
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "products": paginated_products
    }

# -----------------------------
# Sort products by category then price assignment 5
# -----------------------------
@app.get("/products/sort-by-category")
def sort_by_category():

    # Step 1: sort using multiple keys
    sorted_products = sorted(
        products,
        key=lambda x: (x["category"].lower(), x["price"])
    )

    return {
        "products": sorted_products
    }

# -----------------------------
# Browse products (search + sort + paginate) assignment 5
# -----------------------------
@app.get("/products/browse")
def browse_products(
    keyword: str = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):

    result = products.copy()  # work on a copy

    # -----------------------------
    # Step 1: Filter (Search)
    # -----------------------------
    if keyword:
        result = [
            p for p in result
            if keyword.lower() in p["name"].lower()
        ]

    # -----------------------------
    # Step 2: Sort
    # -----------------------------
    if sort_by not in ["price", "name"]:
        return {"error": "sort_by must be 'price' or 'name'"}

    if order not in ["asc", "desc"]:
        return {"error": "order must be 'asc' or 'desc'"}

    reverse = True if order == "desc" else False

    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    # -----------------------------
    # Step 3: Pagination
    # -----------------------------
    total_found = len(result)

    total_pages = (total_found + limit - 1) // limit

    start = (page - 1) * limit
    end = start + limit

    paginated_result = result[start:end]

    # -----------------------------
    # Final Response
    # -----------------------------
    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total_found": total_found,
        "total_pages": total_pages,
        "products": paginated_result
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
        "customer_name": order.company_name,
        "contact_email": order.contact_email,
        "items": [item.dict() for item in order.items],
        "status": "pending"
    }

    orders.append(new_order)

    return new_order

# -----------------------------
# Search orders by customer name assignment 5
# -----------------------------
@app.get("/orders/search")
def search_orders(customer_name: str):

    matched_orders = []

    # loop through all orders
    for order in orders:

        # case-insensitive match
        if customer_name.lower() in order["customer_name"].lower():
            matched_orders.append(order)

    # if no orders found
    if len(matched_orders) == 0:
        return {
            "message": f"No orders found for: {customer_name}"
        }

    return {
        "customer_name": customer_name,
        "total_found": len(matched_orders),
        "orders": matched_orders
    }

# -----------------------------
# Paginate orders assignment 5
# -----------------------------
@app.get("/orders/page")
def paginate_orders(page: int = 1, limit: int = 3):

    # Step 0: validation (optional but good)
    if page < 1 or limit < 1:
        return {"error": "page and limit must be greater than 0"}

    # Step 1: total orders
    total_orders = len(orders)

    # Step 2: total pages
    total_pages = (total_orders + limit - 1) // limit

    # Step 3: slicing indexes
    start = (page - 1) * limit
    end = start + limit

    # Step 4: get paginated orders
    paginated_orders = orders[start:end]

    return {
        "page": page,
        "limit": limit,
        "total_orders": total_orders,
        "total_pages": total_pages,
        "orders": paginated_orders
    }


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

# ==============================
# Day 5: CART SYSTEM
# ==============================

cart = []   # list to store cart items

# -----------------------------
# Add product to cart
# -----------------------------
@app.post("/cart/add")
def add_to_cart(product_id: int, quantity: int = 1):

    # find the product
    product = None
    for p in products:
        if p["id"] == product_id:
            product = p
            break

    # if product doesn't exist
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # check stock
    if not product["in_stock"]:
        raise HTTPException(status_code=400, detail=f"{product['name']} is out of stock")

    # check quantity
    if quantity < 1:
        return {"error": "Quantity must be at least 1"}

    # check if product already in cart
    for item in cart:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            item["subtotal"] = item["quantity"] * product["price"]

            return {
                "message": "Cart updated",
                "cart_item": item
            }

    # new cart item
    cart_item = {
        "product_id": product_id,
        "product_name": product["name"],
        "quantity": quantity,
        "unit_price": product["price"],
        "subtotal": product["price"] * quantity
    }

    cart.append(cart_item)

    return {
        "message": "Added to cart",
        "cart_item": cart_item
    }

# -----------------------------
# View cart items
# -----------------------------
@app.get("/cart")
def view_cart():

    # if cart is empty
    if not cart:
        return {
            "message": "Cart is empty",
            "items": [],
            "item_count": 0,
            "grand_total": 0
        }

    # calculate grand total
    grand_total = 0
    for item in cart:
        grand_total += item["subtotal"]

    return {
        "items": cart,
        "item_count": len(cart),   # number of unique products
        "grand_total": grand_total
    }

# -----------------------------
# Remove item from cart
# -----------------------------
@app.delete("/cart/{product_id}")
def remove_from_cart(product_id: int):

    for item in cart:
        if item["product_id"] == product_id:
            cart.remove(item)

            return {
                "message": f"{item['product_name']} removed from cart"
            }

    raise HTTPException(status_code=404, detail="Product not in cart")

# -----------------------------
# Checkout cart
# -----------------------------
class CheckoutRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    delivery_address: str = Field(..., min_length=10)


@app.post("/cart/checkout")
def checkout(data: CheckoutRequest):

    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")

    placed_orders = []
    grand_total = 0

    for item in cart:

        order_id = len(orders) + 1

        order = {
            "order_id": order_id,
            "customer_name": data.customer_name,
            "product": item["product_name"],
            "quantity": item["quantity"],
            "delivery_address": data.delivery_address,
            "total_price": item["subtotal"],
            "status": "confirmed"
        }

        orders.append(order)
        placed_orders.append(order)
        grand_total += item["subtotal"]

    cart.clear()  # empty cart after checkout

    return {
        "message": "Checkout successful",
        "orders_placed": placed_orders,
        "grand_total": grand_total
    }