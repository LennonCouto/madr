import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.models.author import Author
from app.models.book import Book


@pytest.mark.asyncio
async def test_create_user_db(session: AsyncSession):
    new_user = User(username='alice', password='secret', email='teste@test')

    session.add(new_user)
    await session.commit()

    user = await session.scalar(select(User).where(User.username == 'alice'))

    assert user.username == 'alice'


@pytest.mark.asyncio
async def test_create_book_db(session, author_in_the_db):
    new_book = Book(
        year='1992',
        title='cafe da manha dos campeões',
        author_id=author_in_the_db.id,
    )

    session.add(new_book)
    await session.commit()

    book = await session.scalar(
        select(Book).where(Book.title == 'cafe da manha dos campeões')
    )

    assert book.title == 'cafe da manha dos campeões'


@pytest.mark.asyncio
async def test_create_author_db(session: AsyncSession):
    new_author = Author(
        name='Kurt Vonnegut',
    )

    session.add(new_author)
    await session.commit()

    author = await session.scalar(
        select(Author).where(Author.name == 'Kurt Vonnegut')
    )

    assert author.name == 'Kurt Vonnegut'
