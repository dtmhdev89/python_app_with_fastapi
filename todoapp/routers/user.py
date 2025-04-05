from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, ConfigDict
from passlib.context import CryptContext
from todoapp.database import SessionLocal
from todoapp.routers.auth import get_current_user
from todoapp.models import Users


router = APIRouter(
    prefix="/user",
    tags=["user"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class UserProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str
    username: str
    first_name: str
    last_name: str
    role: str


class UpdateUserPasswordForm(BaseModel):
    old_password: str = Field(min_length=0)
    password: str = Field(min_length=6)
    password_confirmation: str = Field(min_length=6)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(
    user: user_dependency,
    db: db_dependency
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authentication failed"
        )
    
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if user_model is None:
        return None
    
    return UserProfile.model_validate(user_model)


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency,
    db: db_dependency,
    password_form: UpdateUserPasswordForm
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authentication failed"
        )
    hashed_new_password = bcrypt_context.hash(password_form.password)
    new_password_matched = bcrypt_context.verify(
        password_form.password_confirmation,
        hashed_new_password
    )

    if not new_password_matched:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New Password and Password Confirmation did not match"
        )
    
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    verified = bcrypt_context.verify(
        password_form.old_password,
        user_model.hashed_password
    )
    if not verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error on password change"
        )

    user_model.hashed_password = bcrypt_context.hash(password_form.password)
    db.add(user_model)
    db.commit()
