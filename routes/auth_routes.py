from fastapi import APIRouter, HTTPException, status, Depends
from models import UserRegister, UserLogin, Token, UserResponse, UserUpdate
from auth import get_password_hash, verify_password, create_access_token, get_current_user
from database import db
from datetime import datetime
from bson import ObjectId

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=Token)
async def register_user(user: UserRegister):
    database = db.get_db()
    
    # Check if user already exists
    existing_user = await database.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user_dict = {
        "name": user.name,
        "email": user.email,
        "password": get_password_hash(user.password),
        "phone": user.phone,
        "is_admin": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await database.users.insert_one(user_dict)
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.email, "is_admin": False}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login_user(user: UserLogin):
    database = db.get_db()
    
    # Find user
    db_user = await database.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.email, "is_admin": db_user.get("is_admin", False)}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    database = db.get_db()
    
    db_user = await database.users.find_one({"email": current_user["email"]})
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {
        "id": str(db_user["_id"]),
        "name": db_user["name"],
        "email": db_user["email"],
        "phone": db_user.get("phone"),
        "is_admin": db_user.get("is_admin", False),
        "created_at": db_user["created_at"]
    }

@router.put("/me", response_model=UserResponse)
async def update_user_profile(user_update: UserUpdate, current_user: dict = Depends(get_current_user)):
    database = db.get_db()
    
    update_data = {k: v for k, v in user_update.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    result = await database.users.find_one_and_update(
        {"email": current_user["email"]},
        {"$set": update_data},
        return_document=True
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {
        "id": str(result["_id"]),
        "name": result["name"],
        "email": result["email"],
        "phone": result.get("phone"),
        "is_admin": result.get("is_admin", False),
        "created_at": result["created_at"]
    }