from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.core.sanitizers import sanitize_name
from app.models.book import Book
from app.repositories.book_repository import (
    get_by_id_book,
    get_by_title,
    save,
)


async def create_book_service(session, book_schema):
    db_book = await get_by_title(session, book_schema.title)

    if db_book:
        if db_book.title == book_schema.title:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Livro já possui registro',
            )

    book = Book(
        year=book_schema.year,
        title=sanitize_name(book_schema.title),
        author_id=book_schema.author_id,
    )

    save(session, book)
    await session.commit()
    await session.refresh(book)

    return book


async def read_books(session, book_id):
    book_in_the_db = await get_by_id_book(session, book_id)

    if not book_in_the_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Livro não encontrado',
        )

    return book_in_the_db


async def update_book_service(session, book_schema, book_id: int):
    db_book = await get_by_id_book(session, book_id)

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Livro não encontrado'
        )

    for key, value in book_schema.model_dump(exclude_unset=True).items():
        processed_value = value
        if key == 'title':
            processed_value = sanitize_name(value)
        setattr(db_book, key, processed_value)

    try:
        session.add(db_book)
        await session.commit()
        await session.refresh(db_book)
        return db_book

    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Esse titulo já existe'
        )


async def delete_book_with_id_service(session, id_book: int):
    db_book = await get_by_id_book(session, id_book)

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Livro não encontrado'
        )

    await session.delete(db_book)
    await session.commit()

    return {'mensagem': 'Livro excluido da MADR'}
