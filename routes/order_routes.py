from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from models import OrderCreate, OrderResponse, OrderStatusUpdate
from auth import get_current_user, get_current_admin
from database import db
from bson import ObjectId
from datetime import datetime
import random
import string

router = APIRouter(prefix="/api/orders", tags=["Orders"])

def order_helper(order) -> dict:
    return {
        "id": str(order["_id"]),
        "user_id": str(order["user_id"]),
        "order_number": order["order_number"],
        "items": order["items"],
        "shipping_address": order["shipping_address"],
        "payment_method": order["payment_method"],
        "status": order["status"],
        "total": order["total"],
        "notes": order.get("notes"),
        "created_at": order["created_at"],
        "updated_at": order["updated_at"]
    }

def generate_order_number():
    return f"ORD-{''.join(random.choices(string.digits, k=5))}"

@router.post("/", response_model=OrderResponse)
async def create_order(order: OrderCreate, current_user: dict = Depends(get_current_user)):
    database = db.get_db()
    
    # Get user details
    user = await database.users.find_one({"email": current_user["email"]})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Calculate total
    total = sum(item.price * item.quantity for item in order.items)
    
    # Create order
    order_dict = {
        "user_id": user["_id"],
        "order_number": generate_order_number(),
        "items": [item.dict() for item in order.items],
        "shipping_address": order.shipping_address.dict(),
        "payment_method": order.payment_method,
        "status": "pending",
        "total": total,
        "notes": order.notes,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await database.orders.insert_one(order_dict)
    created_order = await database.orders.find_one({"_id": result.inserted_id})
    
    return order_helper(created_order)

@router.get("/my-orders", response_model=List[OrderResponse])
async def get_my_orders(current_user: dict = Depends(get_current_user)):
    database = db.get_db()
    
    user = await database.users.find_one({"email": current_user["email"]})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    orders = await database.orders.find({"user_id": user["_id"]}).sort("created_at", -1).to_list(100)
    return [order_helper(order) for order in orders]

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str, current_user: dict = Depends(get_current_user)):
    database = db.get_db()
    
    if not ObjectId.is_valid(order_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid order ID"
        )
    
    order = await database.orders.find_one({"_id": ObjectId(order_id)})
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Check if user owns this order or is admin
    user = await database.users.find_one({"email": current_user["email"]})
    if str(order["user_id"]) != str(user["_id"]) and not current_user.get("is_admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this order"
        )
    
    return order_helper(order)

# Admin routes
@router.get("/", response_model=List[OrderResponse])
async def get_all_orders(current_user: dict = Depends(get_current_admin), status_filter: Optional[str] = None):
    database = db.get_db()
    
    query = {}
    if status_filter and status_filter != "all":
        query["status"] = status_filter
    
    orders = await database.orders.find(query).sort("created_at", -1).to_list(200)
    return [order_helper(order) for order in orders]

@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(order_id: str, status_update: OrderStatusUpdate, current_user: dict = Depends(get_current_admin)):
    database = db.get_db()
    
    if not ObjectId.is_valid(order_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid order ID"
        )
    
    result = await database.orders.find_one_and_update(
        {"_id": ObjectId(order_id)},
        {
            "$set": {
                "status": status_update.status,
                "updated_at": datetime.utcnow()
            }
        },
        return_document=True
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return order_helper(result)