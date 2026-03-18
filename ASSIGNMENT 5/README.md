# FastAPI Assignment 5 – Advanced Product Browsing & Order Management

## Overview
This assignment focuses on building advanced API functionalities by combining multiple operations such as searching, sorting, and pagination. It also extends order management features by enabling search and pagination on orders, simulating real-world e-commerce backend behavior.

## Technologies Used
- Python
- FastAPI
- Pydantic
- Uvicorn

## Features
- Search products using keyword (case-insensitive)
- Sort products by price or name with configurable order
- Paginate product listings
- Combine search, sort, and pagination in a single endpoint
- Sort products by category and price
- Search orders by customer name
- Paginate orders list for efficient browsing

## 🔗 API Endpoints

| Endpoint | Description |
|--------|--------|
| `GET /products/search/{keyword}` | Search products by keyword (case-insensitive) |
| `GET /products/sort` | Sort products by price or name (asc/desc) |
| `GET /products/page` | Paginate products list |
| `GET /products/sort-by-category` | Sort products by category and price |
| `GET /products/browse` | Combined search, sort, and pagination |
| `GET /orders/search` | Search orders by customer name |
| `GET /orders/page` | Paginate orders list |

## Running the Project

Install dependencies

pip install fastapi uvicorn

Run the FastAPI server

uvicorn main:app --reload

Open interactive API documentation

http://127.0.0.1:8000/docs
