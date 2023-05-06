import random
from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter, Path
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from models import Todos, Users
from database import db
from .auth import get_current_user

router = APIRouter(
    prefix='/user',
    tags=['user']
)


def get_db():
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependancy = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependancy, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Autentication Failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()