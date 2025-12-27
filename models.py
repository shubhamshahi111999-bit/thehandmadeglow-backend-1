from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# User Models
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: Optional[str] = None
    is_admin: bool = False
    created_at: datetime

    class Config:
        json_encoders = {ObjectId: str}

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

# Product Models
class Product(BaseModel):
    name: str
    category: str
    price: int
    original_price: Optional[int] = None
    image: str
    images: List[str] = []
    description: str
    details: str
    wax_type: str
    burn_time: str
    weight: str
    fragrance_notes: List[str]
    rating: float = 4.5
    reviews: int = 0
    in_stock: bool = True
    featured: bool = False
    bestseller: bool = False

class ProductResponse(BaseModel):
    id: str
    name: str
    category: str
    price: int
    original_price: Optional[int] = None
    image: str
    images: List[str] = []
    description: str
    details: str
    wax_type: str
    burn_time: str
    weight: str
    fragrance_notes: List[str]
    rating: float
    reviews: int
    in_stock: bool
    featured: bool
    bestseller: bool

    class Config:
        json_encoders = {ObjectId: str}

# Order Models
class OrderItem(BaseModel):
    product_id: str
    name: str
    price: int
    quantity: int
    image: str

class ShippingAddress(BaseModel):
    name: str
    phone: str
    address: str
    city: str
    state: str
    pincode: str

class OrderCreate(BaseModel):
    items: List[OrderItem]
    shipping_address: ShippingAddress
    payment_method: str
    notes: Optional[str] = None

class OrderResponse(BaseModel):
    id: str
    user_id: str
    order_number: str
    items: List[OrderItem]
    shipping_address: ShippingAddress
    payment_method: str
    status: str
    total: int
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        json_encoders = {ObjectId: str}

class OrderStatusUpdate(BaseModel):
    status: str

# Token Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    is_admin: bool = False