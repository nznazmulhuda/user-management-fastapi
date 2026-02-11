from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.routers import user_routes

# Initialize FastAPI app
app = FastAPI(
    title="User Management API",
    description="A modular FastAPI server with SQLite for user management",
    version="1.0.0",
)

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()
    print("Database initialized successfully!")

# Include routers
app.include_router(user_routes.router)

# Health check endpoint
@app.get("/", tags=["Health"])
def health():
    return {
        "status": "ok",
        "message": "User Management API is running",
        "version": "1.0.0"
    }