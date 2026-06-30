from sqlalchemy import select

from app.models import User
from app.models.book import Book


def test_create_user_db(session):
    new_user = User(username='alice', password='secret', email='teste@test')

    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert user.username == 'alice'


def test_create_book_db(session):
    new_book = Book(year='1992', title='Noite feliz')

    session.add(new_book)
    session.commit()

    book = session.scalar(select(Book).where(Book.title == 'Noite feliz'))

    assert book.title == 'Noite feliz'
