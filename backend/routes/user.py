from fastapi import APIRouter, HTTPException
from bson import json_util
import json
from models.user import UserCreate, UserLogin, UserSettings, Therapist
from utils.cosmos.user_entry import create_user, authenticate_user, get_user_by_id
from utils.cosmos.journal_entry import get_user_entries
from typing import Annotated

router = APIRouter()

@router.post("/register")
async def register(user: UserCreate):
    try:
        user_id = create_user(user)
        return {"success": True, "user_id": str(user_id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(credentials: UserLogin):
    user = authenticate_user(credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"success": True, "user_id": str(user["_id"])}

@router.get("/{user_id}")
async def get_user(user_id: str):
    try:
        user = get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {
            "name": user["name"],
            "email": user["email"],
            "user_type": user["user_type"],
            "settings": user["settings"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/entries/{user_id}")
async def get_journal_entries(user_id: str):
    try:
        entries = get_user_entries(user_id)  # Note: No await needed
        return json.loads(json_util.dumps({
            "entries": entries,
            "count": len(entries)
        }))
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))