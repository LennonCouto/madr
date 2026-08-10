from http import HTTPStatus


def test_create_author(client):
    response = client.post(
        '/author/',
        json={
            'name': 'Kurt Vonnegut',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'name': 'Kurt Vonnegut',
        'id': 1,
    }


def test_create_author_conflict(client, author_in_the_db):
    response = client.post(
        '/author/',
        json={
            'name': 'Kurt Vonnegut',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Author já consta no MADR'}


def test_read_author(client, author_in_the_db):
    response = client.get('/author/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'name': 'Kurt Vonnegut',
        'id': 1,
    }


def test_read_author_not_found(client):
    response = client.get('/author/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author não consta no MADR'}


def test_update_author_success(client, author_in_the_db):
    response = client.patch(
        f'/author/{author_in_the_db.id}',
        json={'name': 'Vonneg Jr'},
    )

    assert response.status_code == HTTPStatus.OK


def test_update_integrity_error(client, author_in_the_db, author_2_in_the_db):
    response = client.patch(
        f'/author/{author_2_in_the_db.id}',
        json={'name': 'Kurt Vonnegut'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Author já consta no MADR'}


def test_update_author_not_found(client):
    response = client.patch(
        '/author/1',
        json={'name': 'Vonneg Jr'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author não consta no MADR'}


def test_delete_author_success(client, author_in_the_db):
    response = client.delete(f'/author/{author_in_the_db.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'mensagem': 'Author deletado do MADR'}


def test_delete_author_not_found(client, author_in_the_db):
    response = client.delete('/author/3')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author não consta no MADR'}
