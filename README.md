# FastAPI_E-Commerce
This is a simple E-commerce API built using FastAPI and MongoDB. It provides endpoints for managing products and orders.This API includes user authentication and offers endpoints to effortlessly create, list, and update products. It also enables order creation and pagination for order listings.

## Features

- User authentication (placeholder).
- Create, list, and update products.
- Create and list orders with pagination.
- Update product quantity.
- Authentication (JWT token generation) - to be implemented.

 ### Prerequisites and Install the required Python packages:

- Python 3.10
- MongoDB (running on default port 27017)
- FastAPI,Uvicorn,PyMongo

  1. Clone the repository:
   ```bash
   git clone https://github.com/sathyark652/FastAPI_E-Commerce.git

  
 2.Start the FastAPI server:
       uvicorn main:app --reload

## Project Structure

- **main.py**: The main FastAPI application file containing route definitions and database connections.
- **models.py**: Defines Pydantic models for User, Product, Item, UserAddress, and Order.
- **README.md**: This README file.

## Usage

##API Documentation
The API documentation (Swagger UI) can be accessed at:
http://127.0.0.1:8000/docs
![image](https://github.com/sathyark652/FastAPI_E-Commerce/assets/117423140/4df5a09d-5e20-4c31-97a9-2526f2efbad0)


## API Endpoints and  REST conventions followed

- POST /login: Authenticate a user and generate an access token.
  ![image](https://github.com/sathyark652/FastAPI_E-Commerce/assets/117423140/6226fb94-e0f2-49ed-8c46-e73af162118f)

- POST /products: Create a new product.
  ![image](https://github.com/sathyark652/FastAPI_E-Commerce/assets/117423140/0ffa296b-e2f7-4c21-8ffe-9e9d643b2853)

- GET /products: List all available products.
- POST /orders: Create a new order.
- GET /orders: List orders with pagination.
- GET /orders/{order_id}: Get a specific order by ID.
- PUT /products/{product_id}: Update the available quantity of a product.


## Structure of MongoDB Collections / Database models

## Data Models in MongoDB:

Users Collection:
You can store user information, such as username, password.

Products Collection:
Store product details, including name, price, and available_quantity.

Orders Collection:
Store order information, including timestamp, items, total_amount, user_id, and status.The items field is an array of subdocuments, where each subdocument represents an ordered item and contains product_id and bought_quantity.
The user_id field establishes a relationship with the users_collection to associate each order with a user.

## Queries to MongoDB:
The MongoDB queries used in this project are straightforward and efficient for the given use cases. Here are some key query operations:

- Insertion: When creating a new product or order, the insert_one method is used to insert the data into the respective collections.

- Retrieval: When listing products or orders, the find method is used to retrieve documents from the collections. Pagination is implemented using skip and limit to control the number of results returned.

- Updating Product Quantity: When updating the available quantity of a product, the update_one method is used to modify the specific document in the products_collection.
- Authentication: When authenticating users, the find_one method is used to search for a user with matching credentials in the users_collection.

## Relationships and Lookups/Joins:

- The primary relationship in the database is between orders and users. Each order document contains a user_id field, which associates the order with a specific user. This allows orders to be retrieved and associated with the corresponding user.

- There are no explicit relationships or joins between products and orders, as orders contain embedded item information that directly references products by their product_id. This denormalized approach optimizes query performance for listing orders with product details.

















  
