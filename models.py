from pydantic import BaseModel

# Define data models
class User(BaseModel):
    username: str
    password: str

class Product(BaseModel):
    name: str
    price: float
    available_quantity: int

class Item(BaseModel):
    product_id: str
    bought_quantity: int

class UserAddress(BaseModel):
    city: str
    country: str
    zip_code: str

class Order(BaseModel):
    timestamp: str
    items: list[Item]
    user_address: UserAddress
    total_amount: float
    user_id: str
    status: str