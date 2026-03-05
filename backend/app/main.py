from fastapi import FastAPI
from app.routes.analyze import router as analyze_router

app = FastAPI(
    title="GitChronicle API",
    description="AI Powered GitHub Project Memory Agent",
    version="1.0"
)

# include routes
app.include_router(analyze_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to GitChronicle API"
    }