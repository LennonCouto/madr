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


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK


def test_update_user_not_found(client):
    response = client.patch(
        '/users/2',
        json={
            'email': 'alice@exemple.com',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado'}


def test_update_user_integrity_error(client, user_in_the_db, user_2_in_the_db):
    response = client.patch(
        '/users/2',
        json={
            'username': 'alice',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Nome ou Email já existe'}


def test_update_success(client, user_in_the_db, user_2_in_the_db):
    response = client.patch(
        '/users/2',
        json={
            'username': 'Jesse',
        },
    )

    assert response.status_code == HTTPStatus.OK


def test_delete_user(client, user_in_the_db):
    response = client.delete(
        '/users/1',
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'mensagem': 'Usuário deletado'}


def test_delete_user_not_found(client):
    response = client.delete(
        '/users/2',
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado'}
