from models.user import UserCreate
from database.database import db
import bcrypt
from bson import ObjectId

collection = db['user']

def create_user(user: UserCreate):
    # Check if user exists
    if collection.find_one({"email": user.email}):
        raise Exception("User already exists")
    
    # Hash password
    hashed = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    
    # Insert user
    result = collection.insert_one({
        **user.dict(exclude={"password"}),
        "password": hashed,
    })
    return result.inserted_id

def authenticate_user(email: str, password: str):
    user = collection.find_one({"email": email})
    if not user:
        return None
    if bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        return user
    return None


def get_user_by_id(user_id: str):
    return collection.find_one({"_id": ObjectId(user_id)})
