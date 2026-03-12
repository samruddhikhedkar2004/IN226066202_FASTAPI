# FastAPI Assignment 3 – CRUD Operations

## Overview
This assignment focuses on implementing full CRUD operations for managing products in a FastAPI-based backend system. The API allows adding new products, updating product details, deleting products, performing inventory audits, and applying category-wide discounts.

## Technologies Used
- Python
- FastAPI
- Pydantic
- Uvicorn

## Features
- Add new products with automatic ID generation
- Prevent duplicate product names
- Update product details using query parameters
- Delete products from the catalogue
- Retrieve product information by ID
- Inventory audit summary for store managers
- Apply category-wide discounts to multiple products

## 🔗 API Endpoints

| Endpoint | Description |
|--------|--------|
| `POST /products` | Add a new product to the catalogue |
| `GET /products` | Retrieve all available products |
| `GET /products/{product_id}` | Retrieve a single product by its ID |
| `PUT /products/{product_id}` | Update product fields such as price or stock status |
| `DELETE /products/{product_id}` | Remove a product from the catalogue |
| `GET /products/audit` | Returns inventory summary including stock counts, out-of-stock products, total stock value, and most expensive product |
| `PUT /products/discount` | Apply a percentage discount to all products within a specific category |

## Running the Project

Install dependencies

pip install fastapi uvicorn

Run the FastAPI server

uvicorn main:app --reload

Open interactive API documentation

http://127.0.0.1:8000/docs
