import os
from fastapi import FastAPI, Request
from todoapp.models import Base
from todoapp.database import engine
from todoapp.routers import auth, todos, admin, user
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()
Base.metadata.create_all(bind=engine)
templates_dir = os.path.join("todoapp", "templates")
templates = Jinja2Templates(directory=templates_dir)
static_files_dir = os.path.join("todoapp", "static")
app.mount("/static", StaticFiles(directory=static_files_dir), name="static")

@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}


@app.get("/")
def test(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(user.router)
