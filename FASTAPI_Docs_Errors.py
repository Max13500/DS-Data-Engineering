from fastapi import FastAPI
from fastapi import Header

from pydantic import BaseModel
from typing import Optional

class Computer(BaseModel):
    """a computer that is available in the store
    """
    computerid: int
    cpu: Optional[str]=None
    gpu: Optional[str]=None
    price: float

api = FastAPI(
    title="My API",
    description="My own API powered by FastAPI.",
    version="1.0.1",
    openapi_tags=[
    {
        'name': 'home',
        'description': 'default functions'
    },
    {
        'name': 'items',
        'description': 'functions that are used to deal with items'
    }
])

@api.get('/',name="Hello World",tags=['home'])
def get_index():
    """Returns greetings
    """
    return {'greetings': 'welcome'}

@api.get('/items', tags=['home', 'items'])
def get_items():
    """returns an item
    """
    return {'item': "some item"}

@api.put('/computer', name='Create a new computer')
def get_computer(computer: Computer):
    """Creates a new computer within the database
    """
    return computer

@api.get('/custom', name='Get custom header')
def get_content(custom_header = Header(None, description='My own personal header')):
    return {
        'Custom-Header': custom_header
    }

# Gestion d'erreurs HTTP
from fastapi import HTTPException
data = [1, 2, 3, 4, 5]

@api.get('/data')
def get_data(index):
    try:
        return {
            'data': data[int(index)]
        }
    except IndexError:
        raise HTTPException(
            status_code=404,
            detail='Unknown Index')
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail='Bad Type'
        )

# Gestion d'erreurs personnalisée
from fastapi import Request
from fastapi.responses import JSONResponse
import datetime

class MyException(Exception):
    def __init__(self,
                 name : str,
                 date: str):
        self.name = name
        self.date = date

@api.exception_handler(MyException)
def MyExceptionHandler(
    request: Request,
    exception: MyException
    ):
    return JSONResponse(
        status_code=418,
        content={
            'url': str(request.url),
            'name': exception.name,
            'message': 'This error is my own',
            'date': exception.date
        }
    )

@api.get('/my_custom_exception')
def get_my_custom_exception():
    raise MyException(
      name='my error',
      date=str(datetime.datetime.now())
      )
    
# Description des réponses / erreurs possibles
responses = {
    200: {"description": "OK"},
    404: {"description": "Item not found"},
    302: {"description": "The item was moved"},
    403: {"description": "Not enough privileges"},
}

@api.get('/thing', responses=responses)
def get_thing():
    return {
        'data': 'hello world'
    }