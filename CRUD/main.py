from fastapi import FastAPI, Request,Response,Form
from fastapi.responses import HTMLResponse
from sqlmodel import Field
from typing import Annotated

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

templates = Jinja2Templates(directory="templates")
