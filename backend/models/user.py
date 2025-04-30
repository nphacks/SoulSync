from pydantic import BaseModel, EmailStr
from typing import Optional

class Therapist(BaseModel):
    name: str = ""
    email: str = ""

class UserSettings(BaseModel):
    therapist: Therapist
    sentimentShare: bool
    emotionShare: bool
    topicShare: bool
    summaryShare: bool
    extremeEmotions: bool

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    user_type: str
    settings: UserSettings

class UserLogin(BaseModel):
    email: EmailStr
    password: str