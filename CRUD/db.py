from dotenv import load_dotenv
from sqlmodel import Field, Session, SQLModel, create_engine, select,delete
import os

load_dotenv('.env')

# sqlite_file_name = "database.db"
sqlite_url = os.getenv('DATABASE_URL')

# connect_args
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str
    img_url: str = ''


class Users(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str
    password: str



def readAllTasks(search:str):
    with Session(engine) as session:
        tasks = []
        if(search != None):
           tasks = session.exec(select(Task)).all()
        if(search != ''):
            tasks = session.exec(select(Task).where(Task.title.like(f'%{search}%'))).all()        
        return tasks

def createTask(newTask:Task):
    with Session(engine) as session:
        session.add(newTask)
        session.commit()
        session.refresh(newTask)
        return newTask

def deleteTask(id:int):
    with Session(engine) as session:
        task = session.exec(delete(Task).where(Task.id == id))
        session.commit()
        return task



def authUser(attemptEmail, attemptPassword):
    # hace query, si encuentra una fila, devuelve userId. Si no, devuelve False
    """ select id from users
        where email = 'bruno@test.com'
        AND password = 'bruno234'        
    """
    with Session(engine) as session:
        userId = session.exec(  select(Users.id).where(Users.email == attemptEmail).where(Users.password == attemptPassword)  ).first()
        print('authUser userId',  userId)
        return userId
    
    ...