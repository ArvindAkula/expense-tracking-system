from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import expenses

# Create FastAPI application
app = FastAPI(
    title="Expense Tracking System",
    description="A FastAPI-based expense tracking system with in-memory database",
    version="1.0.0"
)

# Add CORS middleware to allow cross-origin requests from the Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify your Streamlit frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(expenses.router, prefix="/expenses", tags=["expenses"])


@app.get("/", tags=["root"])
async def read_root():
    """Root endpoint that returns a welcome message."""
    return {"message": "Welcome to the Expense Tracking System API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
