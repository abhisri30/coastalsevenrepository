from fastapi import FastAPI
from app.routes import auth, protected , debug
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="FastAPI with Cognito Authentication")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(protected.router, prefix="/protected", tags=["protected"])
app.include_router(debug.router, prefix="/debug",tags=["debug"])

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI with Cognito"}