from fastapi import FastAPI, Request,Response,Form,HTTPException
from fastapi.responses import HTMLResponse ,RedirectResponse
from sqlmodel import Field
from typing import Annotated

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from db import Task, create_db_and_tables, engine, readAllTasks, createTask, deleteTask, authUser

app = FastAPI()

# ver login
templates = Jinja2Templates(directory="templates")
@app.get("/", response_class=HTMLResponse)
def root(req: Request):
  return templates.TemplateResponse("login.html", {"request": req})


# ver tareas
templates = Jinja2Templates(directory="templates")
@app.get("/tasks", response_class=HTMLResponse)
async def read_item(req: Request,):
    return templates.TemplateResponse("tasks.html", {"request": req})


# Lista temporal para almacenar las tareas
tasks = []
# Agregar tarea
templates = Jinja2Templates(directory="templates")
@app.post("/add-task")
async def add_task(req: Request, task_name: str = Form(...)):
    if not task_name:
        raise HTTPException(status_code=400, detail="El nombre de la tarea no puede estar vacío.")

    try:
        tasks.append(task_name)
    except Exception as e:

        raise HTTPException(status_code=500, detail=f"Error al agregar la tarea: {str(e)}")

    return RedirectResponse(url="/tasks", status_code=303)



# Agregar tarea
templates = Jinja2Templates(directory="templates")
@app.get("/add-task", response_class=HTMLResponse)
async def add_task_page(req: Request):
    return templates.TemplateResponse("add-task.html", {"request": req})
