from http import HTTPStatus


def test_read_root_deve_retornar_ok_e_mensagem(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'subiu!'}


def test_create_user(client):
    response = client.post(
        '/users',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_create_user_username_already_exists(client, user_in_the_db):
    response = client.post(
        '/users/',
        json={
            'username': user_in_the_db.username,
            'email': 'alice@exemple.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Nome de usuario já existe'}


def test_create_user_email_already_exists(client, user_in_the_db):
    response = client.post(
        '/users/',
        json={
            'username': 'bob',
            'email': user_in_the_db.email,
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email já existe'}
