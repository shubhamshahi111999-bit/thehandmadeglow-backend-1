"""
Initialize database with products and admin user
Run this script once to populate the database
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from auth import get_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = "handmade_glow_db"

async def init_database():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    print("🔄 Initializing database...")
    
    # Create admin user
    admin_exists = await db.users.find_one({"email": "admin@thehandmadeglow.com"})
    if not admin_exists:
        admin_user = {
            "name": "Admin User",
            "email": "admin@thehandmadeglow.com",
            "password": get_password_hash("admin123"),
            "phone": "+91 98765 43210",
            "is_admin": True,
            "created_at": None,
            "updated_at": None
        }
        from datetime import datetime
        admin_user["created_at"] = datetime.utcnow()
        admin_user["updated_at"] = datetime.utcnow()
        await db.users.insert_one(admin_user)
        print("✅ Admin user created (email: admin@thehandmadeglow.com, password: admin123)")
    else:
        print("⚠️  Admin user already exists")
    
    # Create products
    products_count = await db.products.count_documents({})
    if products_count == 0:
        products = [
            {
                "name": "Lavender Dreams",
                "category": "relaxation",
                "price": 499,
                "original_price": 699,
                "image": "https://images.unsplash.com/photo-1643122966676-29e8597257f7?w=800",
                "images": [
                    "https://images.unsplash.com/photo-1643122966676-29e8597257f7?w=800",
                    "https://images.unsplash.com/photo-1612198526331-66fcc90d67da?w=800",
                    "https://images.unsplash.com/photo-1572726729207-a78d6feb18d7?w=800"
                ],
                "description": "Immerse yourself in tranquility with our premium lavender-scented candle.",
                "details": "Hand-poured with love, this candle brings the calming essence of fresh lavender fields into your space.",
                "wax_type": "Premium Soy Wax",
                "burn_time": "40-45 hours",
                "weight": "200g",
                "fragrance_notes": ["Lavender", "Vanilla", "Chamomile"],
                "rating": 4.8,
                "reviews": 127,
                "in_stock": True,
                "featured": True,
                "bestseller": True
            },
            {
                "name": "Vanilla Bliss",
                "category": "relaxation",
                "price": 449,
                "original_price": 599,
                "image": "https://images.unsplash.com/photo-1612293905607-b003de9e54fb?w=800",
                "images": ["https://images.unsplash.com/photo-1612293905607-b003de9e54fb?w=800"],
                "description": "Sweet vanilla warmth wrapped in soft, creamy notes.",
                "details": "Perfect for creating a cozy atmosphere, this vanilla candle is comfort in a jar.",
                "wax_type": "Premium Soy Wax",
                "burn_time": "35-40 hours",
                "weight": "180g",
                "fragrance_notes": ["Vanilla", "Cream", "Honey"],
                "rating": 4.9,
                "reviews": 203,
                "in_stock": True,
                "featured": True,
                "bestseller": True
            },
            {
                "name": "Festive Spice",
                "category": "festive",
                "price": 549,
                "original_price": 749,
                "image": "https://images.pexels.com/photos/1832562/pexels-photo-1832562.jpeg?w=800",
                "images": ["https://images.pexels.com/photos/1832562/pexels-photo-1832562.jpeg?w=800"],
                "description": "Celebrate every moment with this warm, spicy festive candle.",
                "details": "Infused with cinnamon, clove, and orange peel for that perfect holiday feeling.",
                "wax_type": "Premium Soy Wax",
                "burn_time": "45-50 hours",
                "weight": "220g",
                "fragrance_notes": ["Cinnamon", "Clove", "Orange"],
                "rating": 4.7,
                "reviews": 89,
                "in_stock": True,
                "featured": True,
                "bestseller": False
            },
            {
                "name": "Rose Garden",
                "category": "relaxation",
                "price": 499,
                "original_price": None,
                "image": "https://images.pexels.com/photos/6755790/pexels-photo-6755790.jpeg?w=800",
                "images": ["https://images.pexels.com/photos/6755790/pexels-photo-6755790.jpeg?w=800"],
                "description": "Elegant rose fragrance with hints of jasmine.",
                "details": "A luxurious blend that brings the beauty of a blooming garden indoors.",
                "wax_type": "Premium Soy Wax",
                "burn_time": "38-42 hours",
                "weight": "200g",
                "fragrance_notes": ["Rose", "Jasmine", "Peony"],
                "rating": 4.6,
                "reviews": 54,
                "in_stock": True,
                "featured": False,
                "bestseller": False
            },
            {
                "name": "Ocean Breeze",
                "category": "relaxation",
                "price": 479,
                "original_price": None,
                "image": "https://images.unsplash.com/photo-1612198526331-66fcc90d67da?w=800",
                "images": ["https://images.unsplash.com/photo-1612198526331-66fcc90d67da?w=800"],
                "description": "Fresh and invigorating ocean-inspired fragrance.",
                "details": "Brings the calming essence of sea breeze right to your home.",
                "wax_type": "Premium Soy Wax",
                "burn_time": "40-44 hours",
                "weight": "200g",
                "fragrance_notes": ["Sea Salt", "Ozone", "Driftwood"],
                "rating": 4.5,
                "reviews": 76,
                "in_stock": True,
                "featured": False,
                "bestseller": True
            },
            {
                "name": "Sandalwood Serenity",
                "category": "relaxation",
                "price": 529,
                "original_price": None,
                "image": "https://images.unsplash.com/photo-1572726729207-a78d6feb18d7?w=800",
                "images": ["https://images.unsplash.com/photo-1572726729207-a78d6feb18d7?w=800"],
                "description": "Warm, woody sandalwood for deep relaxation.",
                "details": "Perfect for meditation and unwinding after a long day.",
                "wax_type": "Premium Soy Wax",
                "burn_time": "42-48 hours",
                "weight": "210g",
                "fragrance_notes": ["Sandalwood", "Cedar", "Amber"],
                "rating": 4.8,
                "reviews": 112,
                "in_stock": True,
                "featured": True,
                "bestseller": False
            },
            {
                "name": "Citrus Sunrise",
                "category": "festive",
                "price": 459,
                "original_price": None,
                "image": "https://images.unsplash.com/photo-1643122966676-29e8597257f7?w=800",
                "images": ["https://images.unsplash.com/photo-1643122966676-29e8597257f7?w=800"],
                "description": "Bright and uplifting citrus blend.",
                "details": "Start your day with this energizing mix of orange, lemon, and grapefruit.",
                "wax_type": "Premium Soy Wax",
                "burn_time": "36-40 hours",
                "weight": "190g",
                "fragrance_notes": ["Orange", "Lemon", "Grapefruit"],
                "rating": 4.7,
                "reviews": 98,
                "in_stock": True,
                "featured": False,
                "bestseller": False
            },
            {
                "name": "Gift Set - Tranquility",
                "category": "gift",
                "price": 1299,
                "original_price": 1699,
                "image": "https://images.unsplash.com/photo-1646562011038-73774c1ef7d7?w=800",
                "images": ["https://images.unsplash.com/photo-1646562011038-73774c1ef7d7?w=800"],
                "description": "Beautiful gift set with 3 handpicked candles.",
                "details": "Includes Lavender Dreams, Vanilla Bliss, and Sandalwood Serenity in a premium gift box.",
                "wax_type": "Premium Soy Wax",
                "burn_time": "120+ hours (combined)",
                "weight": "600g (3x200g)",
                "fragrance_notes": ["Lavender", "Vanilla", "Sandalwood"],
                "rating": 5.0,
                "reviews": 45,
                "in_stock": True,
                "featured": True,
                "bestseller": True
            }
        ]
        
        await db.products.insert_many(products)
        print(f"✅ {len(products)} products created")
    else:
        print(f"⚠️  Database already has {products_count} products")
    
    print("✅ Database initialization complete!")
    client.close()

if __name__ == "__main__":
    asyncio.run(init_database())
