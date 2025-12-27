from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from models import Product, ProductResponse
from auth import get_current_admin
from database import db
from bson import ObjectId

router = APIRouter(prefix="/api/products", tags=["Products"])

def product_helper(product) -> dict:
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "category": product["category"],
        "price": product["price"],
        "original_price": product.get("original_price"),
        "image": product["image"],
        "images": product.get("images", []),
        "description": product["description"],
        "details": product["details"],
        "wax_type": product["wax_type"],
        "burn_time": product["burn_time"],
        "weight": product["weight"],
        "fragrance_notes": product["fragrance_notes"],
        "rating": product.get("rating", 4.5),
        "reviews": product.get("reviews", 0),
        "in_stock": product.get("in_stock", True),
        "featured": product.get("featured", False),
        "bestseller": product.get("bestseller", False)
    }

@router.get("/", response_model=List[ProductResponse])
async def get_all_products(category: Optional[str] = None):
    database = db.get_db()
    
    query = {}
    if category and category != "all":
        query["category"] = category
    
    products = await database.products.find(query).to_list(100)
    return [product_helper(product) for product in products]

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    database = db.get_db()
    
    if not ObjectId.is_valid(product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID"
        )
    
    product = await database.products.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return product_helper(product)

@router.post("/", response_model=ProductResponse)
async def create_product(product: Product, current_user: dict = Depends(get_current_admin)):
    database = db.get_db()
    
    product_dict = product.dict()
    result = await database.products.insert_one(product_dict)
    
    created_product = await database.products.find_one({"_id": result.inserted_id})
    return product_helper(created_product)

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: str, product: Product, current_user: dict = Depends(get_current_admin)):
    database = db.get_db()
    
    if not ObjectId.is_valid(product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID"
        )
    
    product_dict = product.dict()
    result = await database.products.find_one_and_update(
        {"_id": ObjectId(product_id)},
        {"$set": product_dict},
        return_document=True
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return product_helper(result)

@router.delete("/{product_id}")
async def delete_product(product_id: str, current_user: dict = Depends(get_current_admin)):
    database = db.get_db()
    
    if not ObjectId.is_valid(product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID"
        )
    
    result = await database.products.delete_one({"_id": ObjectId(product_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return {"message": "Product deleted successfully"}