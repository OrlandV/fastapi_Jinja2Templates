from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from typing import Annotated

app = FastAPI()
templates = Jinja2Templates('templates')
users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int = 18


@app.get('/')
async def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get('/users/{user_id}')
async def get_users(request: Request, user_id: int = Path(ge=1, le=100, description='Enter User ID', example=1)
                    ) -> HTMLResponse:
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse('users.html', {'request': request, 'user': user})
    raise HTTPException(404, 'User was not found.')


@app.post('/user/{username}/{age}')
async def create_user(
    username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='User1')],
    age: int = Path(ge=18, le=120, description='Enter age', example=20)
) -> User:
    user = User(
        id=users[-1].id + 1 if len(users) > 0 else 1,
        username=username,
        age=age
    )
    users.append(user)
    return user


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(
    user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example=1)],
    username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='User1')],
    age: int = Path(ge=18, le=120, description='Enter age', example=20)
) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(404, 'User was not found.')


@app.delete('/user/{user_id}')
async def delete_user(user_id: int = Path(ge=1, le=100, description='Enter User ID', example=1)) -> User:
    for i in range(len(users)):
        if users[i].id == user_id:
            return users.pop(i)
    raise HTTPException(404, 'User was not found.')
