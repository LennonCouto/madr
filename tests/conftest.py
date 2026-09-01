import factory
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from testcontainers.postgres import PostgresContainer

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


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:18', driver='psycopg') as postgres:
        yield create_async_engine(postgres.get_connection_url())


@pytest_asyncio.fixture
async def session(engine):
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@pytest.fixture
def token(client, user_in_the_db):
    response = client.post(
        '/auth/login',
        data={
            'username': user_in_the_db.email,
            'password': user_in_the_db.clean_password,
        },
    )

    return response.json()['access_token']


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}_password')


@pytest_asyncio.fixture
async def user_in_the_db(session):
    password = 'password123'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password
    return user


@pytest_asyncio.fixture
async def user_2_in_the_db(session):
    user = UserFactory(password=get_password_hash('password123'))

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


@pytest_asyncio.fixture
async def book_in_the_db(session, author_in_the_db):
    book = Book(
        year='1973',
        title='Café Da Manha Dos Campeões',
        author_id=author_in_the_db.id,
    )

    session.add(book)
    await session.commit()
    await session.refresh(book)

    return book


@pytest_asyncio.fixture
async def book_2_in_the_db(session, author_2_in_the_db):
    book = Book(
        year='1993',
        title='O Ladrão De Casaca',
        author_id=author_2_in_the_db.id,
    )

    session.add(book)
    await session.commit()
    await session.refresh(book)

    return book


@pytest_asyncio.fixture
async def author_in_the_db(session):
    author = Author(name='Kurt Vonnegut')

    session.add(author)
    await session.commit()
    await session.refresh(author)

    return author


@pytest_asyncio.fixture
async def author_2_in_the_db(session: AsyncSession):
    author = Author(name='Maurice Leblanc')

    session.add(author)
    await session.commit()
    await session.refresh(author)

    return author
