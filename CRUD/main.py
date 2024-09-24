from fastapi import FastAPI, Request,Response,Form,HTTPException
from fastapi.responses import HTMLResponse ,RedirectResponse
from sqlmodel import Field, Session, SQLModel, create_engine, select, delete
from typing import Annotated

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from db import Task, create_db_and_tables, engine, readAllTasks, createTask, deleteTask,updateTask, authUser

app = FastAPI()
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

#### ver login
templates = Jinja2Templates(directory="templates")
@app.get("/", response_class=HTMLResponse)
def root(request: Request):
  return templates.TemplateResponse("login.html", {"request": request})


### Función para autenticar
def getAuthUserId(cookies):
    if 'cookieUserId' in cookies.keys(): 
        return cookies['cookieUserId']
    return False
 

########## Autenticación ###########
@app.post("/login")
async def authlogin(email: Annotated[str, Form()], password: Annotated[str, Form()], res:Response):

    authenticatedUserId = authUser(email,password) 

    if authenticatedUserId != None:
        #res.set_cookie('cookieUserId', authenticatedUserId)
        response = RedirectResponse(url="/tasks", status_code=303)
        response.set_cookie('cookieUserId', authenticatedUserId)
        return response
                                                
    res.status_code = 400
    return 'Credenciales inválidas. Reintente nuevamente.'

########## Logout ###########
@app.get("/logout")
async def authlogout(res:Response):
    print("Eliminando cookie")
    # res.delete_cookie('cookieUserId')
    print("Cookie eliminada")
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie('cookieUserId')
    return response

"""
res.status_code = 200
res.set_cookie('cookieUserId', authenticatedUserId)
return 'Login exitoso!'
"""


####funcion para autenticacion##
def require_authentication(request: Request):
    if 'cookieUserId' not in request.cookies:
        raise HTTPException(status_code=403, detail="No autenticado")
    return request.cookies['cookieUserId']

# ver tareas
templates = Jinja2Templates(directory="templates")
@app.get("/tasks", response_class=HTMLResponse)
async def root(request: Request, search: str = ''):
    user_id = require_authentication(request)
    tasks = readAllTasks(search) 
    return templates.TemplateResponse("tasks.html", {"request": request,"tasks": tasks})


# Agregar tarea
templates = Jinja2Templates(directory="templates")
@app.get("/add-task", response_class=HTMLResponse)
async def add_task_page(request: Request):
    user_id = require_authentication(request)
    return templates.TemplateResponse("add-task.html", {"request": request})

@app.post("/add-task")
async def add_task(request: Request, title: str = Form(...), description: str = Form(...), img_url: str = Form(...)):
    user_id = require_authentication(request)
    new_task = Task(title=title, description=description, img_url=img_url)

    try:
        createTask(new_task)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al agregar la tarea: {str(e)}")

    return RedirectResponse(url="/tasks", status_code=303)

# Editar tarea
@app.get("/edit-task/{task_id}", response_class=HTMLResponse)
async def edit_task_page(request: Request, task_id: int):
    user_id = require_authentication(request)
    with Session(engine) as session:
        task = session.exec(select(Task).where(Task.id == task_id)).first()
        if not task:
            raise HTTPException(status_code=404, detail="Tarea no encontrada.")
    
    return templates.TemplateResponse("edit-task.html", {"request": request, "task": task})

@app.post("/edit-task/{task_id}")
async def edit_task(request: Request, task_id: int, title: str = Form(...), description: str = Form(...), img_url: str = Form(...)):
    user_id = require_authentication(request)
    updated_task = Task(id=task_id, title=title, description=description, img_url=img_url)
    
    try:
        updateTask(updated_task)  # Llama a la función para actualizar la tarea
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al editar la tarea: {str(e)}")
    
    return RedirectResponse(url="/tasks", status_code=303)

# borrar tarea
@app.post("/delete-task/{task_id}")
async def delete_task(task_id: int):
    user_id = require_authentication(request)
    try:
        deleteTask(task_id)  # Llama a la función para eliminar la tarea
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar la tarea: {str(e)}")
    
    return RedirectResponse(url="/tasks", status_code=303)





