# FastAPI Assignment 4 – Cart System & Checkout Workflow

## Overview
This assignment focuses on implementing a complete shopping cart system using FastAPI. It includes adding products to the cart, viewing cart contents, removing items, handling out-of-stock scenarios, and completing the checkout process while creating orders.

## Technologies Used
- Python
- FastAPI
- Pydantic
- Uvicorn

## Features
- Add products to the cart with quantity
- Prevent adding out-of-stock products
- View cart items with calculated subtotals
- Calculate grand total automatically
- Remove items from the cart
- Checkout cart items and create orders
- Handle checkout with empty cart gracefully
- Maintain order history after checkout

## 🔗 API Endpoints

| Endpoint | Description |
|--------|--------|
| `POST /cart/add` | Add a product to the shopping cart with quantity |
| `GET /cart` | View all items currently in the cart along with grand total |
| `DELETE /cart/{product_id}` | Remove a specific product from the cart |
| `POST /cart/checkout` | Checkout cart items and convert them into orders |
| `GET /orders` | View all placed orders |

## Running the Project

Install dependencies

pip install fastapi uvicorn

Run the FastAPI server

uvicorn main:app --reload

Open interactive API documentation

http://127.0.0.1:8000/docs
