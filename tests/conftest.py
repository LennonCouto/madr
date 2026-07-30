import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.core.security import get_password_hash
from app.db.registry import table_registry
from app.db.session import get_session
from app.main import app
from app.models import User
from app.models.author import Author
from app.models.book import Book


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def token(client, user_in_the_db):
    response = client.post(
        '/login',
        data={
            'username': user_in_the_db.email,
            'password': user_in_the_db.clean_password,
        },
    )

    return response.json()['access_token']


@pytest.fixture
def user_in_the_db(session):
    password = 'password123'

    user = User(
        username='Alice',
        email='alice@example.com',
        password=get_password_hash(password),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password
    return user


@pytest.fixture
def user_2_in_the_db(session):
    user = User(
        username='bob', email='bob@example.com', password='password123'
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture
def book_in_the_db(session, author_in_the_db):
    book = Book(
        year='1973',
        title='Café Da Manha Dos Campeões',
        author_id=author_in_the_db.id,
    )

    session.add(book)
    session.commit()
    session.refresh(book)

    return book


@pytest.fixture
def book_2_in_the_db(session, author_2_in_the_db):
    book = Book(
        year='1993',
        title='O Ladrão De Casaca',
        author_id=author_2_in_the_db.id,
    )

    session.add(book)
    session.commit()
    session.refresh(book)

    return book


@pytest.fixture
def author_in_the_db(session):
    author = Author(name='Kurt Vonnegut')

    session.add(author)
    session.commit()
    session.refresh(author)

    return author


@pytest.fixture
def author_2_in_the_db(session):
    author = Author(name='Maurice Leblanc')

    session.add(author)
    session.commit()
    session.refresh(author)

    return author
