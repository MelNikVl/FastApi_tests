import random
from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from models import Todos
from database import db

router = APIRouter()


def get_db():
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@router.get("/")
async def read_all(db: db_dependency):
    return db.query(Todos).all()


@router.get("/todo/{todo_id}")
async def read_todo(db: db_dependency, todo_id: int):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.dict())

    db.add(todo_model)
    db.commit()

    return f'создание карточки прошло успешно'


@router.put("/todo/{todo_id}")
async def update_todo(db: db_dependency,
                      todo_id: int,
                      todo_request: TodoRequest):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@router.get("/check_complete")
async def check_complete(zapros_k_base: db_dependency,
                         todo_id: bool):
    todo_model = zapros_k_base.query(Todos).filter(Todos.complete == todo_id).all()
    return todo_model


@router.delete("/delete")
async def delete(zapros_k_base: db_dependency,
                 todo_id: int):
    delete_query = zapros_k_base.query(Todos).filter(Todos.id == todo_id).first()
    db.delete(delete_query)
    db.commit()

    return f'удаление карточки {todo_id} прошло успешно'


@router.delete("/delete_all")
async def udalenie_vsego_k_huyam(zapros_k_base: db_dependency):
    zapros_k_base.query(Todos).delete()
    db.commit()

    return f'удаление ВСЕХ карточек прошло успешно'


@router.post("/create_5_cards_uncomplete")
async def create_todo_uncomplete(db: db_dependency):
    for i in range(5):
        todo_example = Todos(
            title="title",
            description="description",
            priority="5",
            complete=False,
        )

        db.add(todo_example)
        db.commit()

    return f'создание 5 незавершенных карточек прошло успешно'


@router.post("/create_5_cards_complete")
async def create_todo_complete(db: db_dependency):
    for i in range(5):
        random_number = random.randint(1, 5)
        todo_example = Todos(
            title="title",
            description="description",
            priority=random_number,
            complete=True,
        )

        db.add(todo_example)
        db.commit()

    return f'создание 5 завершенных карточек прошло успешно'
