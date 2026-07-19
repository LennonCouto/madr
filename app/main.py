from fastapi import FastAPI

from app.routers import auth, author, book, user

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(book.router)
app.include_router(author.router)
