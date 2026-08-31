import asyncio
import sys

from fastapi import FastAPI

from app.routers import auth, author, book, user

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


app = FastAPI(swagger_ui_parameters={'syntaxHighlight': {'theme': 'obsidian'}})

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(book.router)
app.include_router(author.router)
