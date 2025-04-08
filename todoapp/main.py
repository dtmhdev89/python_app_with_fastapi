import os
from fastapi import FastAPI, Request, status
from todoapp.models import Base
from todoapp.database import engine
from todoapp.routers import auth, todos, admin, user
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse


app = FastAPI()
Base.metadata.create_all(bind=engine)
static_files_dir = os.path.join("todoapp", "static")
app.mount("/static", StaticFiles(directory=static_files_dir), name="static")

@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}


@app.get("/")
def test(request: Request):
    return RedirectResponse(
        url="/todos/todo-page",
        status_code=status.HTTP_302_FOUND
    )

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(user.router)
