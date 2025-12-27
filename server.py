from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from database import db
from routes import auth_routes, product_routes, order_routes

load_dotenv()

app = FastAPI(title="The Handmade Glow API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*","https://thehandmadeglow-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup and shutdown events
@app.on_event("startup")
async def startup_db_client():
    await db.connect_db()
    print("✅ Backend server started successfully")

@app.on_event("shutdown")
async def shutdown_db_client():
    await db.close_db()

# Include routers
app.include_router(auth_routes.router)
app.include_router(product_routes.router)
app.include_router(order_routes.router)

@app.get("/api/")
async def root():
    return {"message": "The Handmade Glow API is running!", "status": "healthy"}
