from fastapi import FastAPI

from madr.routers import contas

app = FastAPI()

app.include_router(contas.router)


@app.get('/')
def read():
    return {'message': 'subiu!'}
