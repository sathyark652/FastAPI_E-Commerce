# main.py

# (imports and MongoDB connection)
from fastapi import FastAPI, HTTPException, Query, Depends
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel
from datetime import datetime
import models



app = FastAPI()

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce"]#create database in mongodb named ecommerce

# create collections in mongodb and use it 
products_collection = db["products"]
orders_collection = db["orders"]
users_collection = db["users"]  


# Authentication 
def authenticate_user(username: str, password: str):
    # Implement user authentication logic here (e.g., check against a user database)
    user = users_collection.find_one({"username": username, "password": password})
    return user is not None

def get_current_user(username: str = Depends(authenticate_user)):
    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return username
    


#login route
@app.post("/login")
async def login(user_credentials: models.User):
    """
    Authenticate a user and generate an access token.

    Args:
        user_credentials (User): User's login credentials.

    Returns:
        dict: Access token and token type.
    """
    if authenticate_user(user_credentials.username, user_credentials.password):
        ## Placeholder code for generating JWT token
        token = "your_generated_token_here"
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Login failed")
    
    
    
# Create product
@app.post("/products")
async def create_product(product: models.Product):
    product_id = products_collection.insert_one(product.dict()).inserted_id
    return {"message": "Product created successfully", "product_id": str(product_id)}
    
    

# 1)List all available products in the system
@app.get("/products")
async def list_products():
    products = products_collection.find()
    
    # Convert ObjectId to string for JSON serialization
    products = [dict(product, _id=str(product["_id"])) for product in products]
    
    return products
    
async def get_product(product_id: str):
    try:
        product = products_collection.find_one({"_id": ObjectId(product_id)})
        if product:
            product['_id'] = str(product['_id'])  # Convert ObjectId to string
            return product
        raise HTTPException(status_code=404, detail=f"Product with ID {item['product_id']} not found")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
        

# 2)Create order
@app.post("/orders")
async def create_order(order: models.Order, current_user: str = Depends(get_current_user)):
    total_amount = 0
    
    # Convert the order object to a dictionary
    order_dict = order.dict()
    
    # Iterate through order items, converting them to dictionaries as well
    for item in order_dict["items"]:
        product = await get_product(ObjectId(item["product_id"]))
        if product:
            total_amount += item["bought_quantity"] * product["price"]
        else:
            raise HTTPException(status_code=404, detail=f"Product with ID {item['product_id']} not found")
    
    # Update the total_amount in the order dictionary
    order_dict["total_amount"] = total_amount
    
    # Add other fields like timestamp, user_id, and status to the order dictionary
    order_dict["timestamp"] = datetime.now().isoformat()
    order_dict["user_id"] = current_user
    order_dict["status"] = "pending"
    
    # Insert the order dictionary into the orders_collection
    order_id = orders_collection.insert_one(order_dict).inserted_id
    
    return {"message": "Order created successfully", "order_id": str(order_id)}
    
    
    

# 3)List orders with pagination
@app.get("/orders")
async def list_orders(limit: int = Query(10, le=100), offset: int = Query(0, ge=0)):
    # Query orders from MongoDB with pagination
    orders = orders_collection.find().skip(offset).limit(limit)
    
    # Convert ObjectId to string for JSON serialization
    orders = [dict(order, _id=str(order["_id"])) for order in orders]
    
    return orders



# 4)Get order by ID
@app.get("/orders/{order_id}")
async def get_order(order_id: str):
    try:
        order = orders_collection.find_one({"_id": ObjectId(order_id)})
        if order:
            order['_id'] = str(order['_id'])  # Convert ObjectId to string
            return order
        raise HTTPException(status_code=404, detail="Order not found")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))



# 5)Update product quantity
@app.put("/products/{product_id}")
async def update_product_quantity(product_id: str, new_quantity: int):
    try:
        # Convert product_id to ObjectId
        product_id = ObjectId(product_id)
        
        result = products_collection.update_one(
            {"_id": product_id},
            {"$set": {"available_quantity": new_quantity}}
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")

        return {"message": "Product quantity updated successfully"}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
        

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
#The app will be running at http://127.0.0.1:8000/ (localhost )
# check http://127.0.0.1:8000/docs#/ for testing the api results and schemas
