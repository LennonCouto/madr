from http import HTTPStatus

from jwt import decode

from app.core.config import settings
from app.core.security import create_access_token


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(token, settings.SECRET_KEY, algorithms=['HS256'])

    assert decoded['test'] == data['test']
    assert 'exp' in decoded


def test_get_token(client, user_in_the_db):
    response = client.post(
        '/login',
        data={
            'username': user_in_the_db.email,
            'password': user_in_the_db.clean_password,
        },
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token
