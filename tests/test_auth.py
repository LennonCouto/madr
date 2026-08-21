from http import HTTPStatus

from freezegun import freeze_time


def test_token_expired_after_time(client, user_in_the_db):
    with freeze_time('1992-03-09 12:00:00'):
        response = client.post(
            '/login',
            data={
                'username': user_in_the_db.email,
                'password': user_in_the_db.clean_password,
            },
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('1992-03-09 12:31:00'):
        response = client.patch(
            f'/users/{user_in_the_db.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'new_username',
                'email': 'new_email@example.com',
                'password': 'new_password',
            },
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {
            'detail': 'Você não possui credenciais válidas'
        }


def test_token_inexistent_user(client):
    response = client.post(
        '/login',
        data={
            'username': 'nonexistent@example.com',
            'password': 'wrong_password',
        }
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_wrong_password(client, user_in_the_db):
    response = client.post(
        '/login',
        data={
            'username': user_in_the_db.email,
            'password': 'wrong_password',
        }
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}
