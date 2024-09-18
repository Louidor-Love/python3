from fastapi import FastAPI, Request,Response,Form
from fastapi.responses import HTMLResponse ,RedirectResponse
from sqlmodel import Field
from typing import Annotated

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from db import Task, create_db_and_tables, engine, readAllTasks, createTask, deleteTask, authUser

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def root(req: Request):
  return templates.TemplateResponse("login.html", {"request": req})









