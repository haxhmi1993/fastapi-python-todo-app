from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from config.db.database_config import get_db
from .models import Todos
from common.responses.responses import success_response
from common.exceptions.httpexception import http_exception
from .schemas.todo import Todo
from .schemas.todo_update import UpdateTodo


router = APIRouter(
    prefix='/todos',
    tags=['todos'],
    responses={404: {"description": "Not Found"}}
)


@router.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(Todos).all()


@router.get("/{todo_id}")
async def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo is None:
        raise http_exception(404,  f'Todo with {todo_id} not found')
    return todo


@router.post("/")
async def create_todo(todo: Todo, db: Session = Depends(get_db)):
    todo_model = Todos(**todo.model_dump())
    db.add(todo_model)
    db.commit()

    return success_response(201)


@router.put('/{todo_id}')
async def update_todo(todo_id: int,  todo: UpdateTodo, db: Session = Depends(get_db)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id)
    todo_model_found = todo_model.first()
    if todo_model_found is None:
        raise http_exception(404, f'Todo with id {todo_id} not found')

    todo_model.update(todo.model_dump(exclude_unset=True),
                      synchronize_session=False)
    db.commit()

    return success_response(201)


@router.delete("/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise http_exception(404,  f'Todo with id {todo_id} not found')
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()

    return success_response(200)
