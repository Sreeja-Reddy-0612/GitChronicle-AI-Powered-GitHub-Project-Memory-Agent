from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.routes.analyze import router as analyze_router

app = FastAPI(
    title="GitChronicle API",
    description="AI-powered GitHub repository evolution analyzer",
    version="1.0.0"
)

app.include_router(analyze_router)


@app.get("/")
def root():
    return {"message": "GitChronicle backend running"}