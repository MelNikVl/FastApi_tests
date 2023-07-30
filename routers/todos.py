from __future__ import annotations
import random
from typing import Annotated, Optional, List
from fastapi import Depends, HTTPException, APIRouter, Path, Request, UploadFile, File
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import HTMLResponse
from models import Todos
from database import db
from .auth import get_current_user
import datetime
import os
from fastapi.templating import Jinja2Templates
import shutil
from typing import Any, Dict

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def get_db():
    try:
        yield db
    finally:
        db.close()

def response(data: Any, status: bool = True):
    if data is None:
        data = {}
    return {"data": data, "status": status}


db_dependency = Annotated[Session, Depends(get_db)]
user_dependancy = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Todos).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependancy, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Autentication Failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id) \
        .filter(Todos.owner_id == user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(
                      db: db_dependency,
                      todo_request: TodoRequest):
    # if user is None:
    #     raise HTTPException(status_code=401, detail="Authentication_Failed")
    todo_model = Todos(**todo_request.dict(), owner_id=1)

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
    return response(data={"message": f'создание 5 незавершенных карточек прошло успешно'})


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

@router.post("/file_download")
async def send_to_trash_finally(invoce: UploadFile = File(...)):
    timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))
    destination_folder = os.path.join("\\\\fs-mo\\ADMINS\\Photo_warehouse\\archive_after_utilization", timestamp)
    os.makedirs(destination_folder, exist_ok=True)

    out_filename = os.path.join(destination_folder, invoce.filename)

    with open(out_filename, "wb") as buffer:
        buffer.write(await invoce.read())

@router.post("/uploadfiles/")
async def create_upload_files(material: str = "lj",
                              material_id: int = 0,
                              files: UploadFile = None):
    print(files)
    return material, material_id, files


@router.post("/uploadfiles1/")
async def create_upload_files1(material_id:int = 0, files: List[UploadFile] = File(None)):
    # return {"filenames": [file.filename for file in files]}
    # else:
    print(files)
    return "test ok"
        # return {"status": False, "test": "File not attached"}


@router.get("/test_button")
async def main(request: Request = None):
    out = "fdsfds"
    return templates.TemplateResponse("test.html", {"request": request, "data": out})
