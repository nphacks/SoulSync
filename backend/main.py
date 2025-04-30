# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user import router as items_router
from routes.journal_entry import router as journal_router
from routes.bot import router as bot_router
from routes.report import router as report_router
from routes.user import router as user_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular dev server
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(items_router, prefix="/items", tags=["items"])
app.include_router(journal_router, prefix="/journal_entry", tags=["journal"])
app.include_router(bot_router, prefix="/chatbot", tags=["chat"])
app.include_router(report_router, prefix="/report", tags=["adx"])
app.include_router(user_router, prefix="/users", tags=["user"])

@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI app!"}