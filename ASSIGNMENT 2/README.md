# FastAPI Assignment 2 – Product & Order Management API

## Overview
This project is a simple FastAPI-based backend API that simulates a small e-commerce system.  
It includes product filtering, price lookup, customer feedback submission, bulk order processing, and order status tracking.

## Technologies Used
- Python
- FastAPI
- Pydantic
- Uvicorn

## Features
- Filter products using query parameters
- Get product price using path parameters
- Product summary dashboard
- Customer feedback submission with validation
- Bulk order placement with stock checking
- Order status tracking (pending → confirmed)

## API Endpoints

GET /products/filter  
Filter products by category and price range.

GET /products/{product_id}/price  
Get only the name and price of a product.

GET /products/summary  
Returns store statistics including total products, stock count, cheapest and most expensive product, and categories.

POST /feedback  
Submit customer feedback for a product.

POST /orders/bulk  
Place a bulk order with multiple items.

POST /orders  
Create a new order with status "pending".

GET /orders/{order_id}  
Retrieve order details by order ID.

PATCH /orders/{order_id}/confirm  
Update order status from "pending" to "confirmed".

## Running the Project

Install dependencies

pip install fastapi uvicorn

Run the server

uvicorn main:app --reload

Open API documentation

http://127.0.0.1:8000/docs

B.Tech Electronics and Telecommunication Engineering
