from http import HTTPStatus


def test_create_book(client):
    response = client.post(
        '/book/',
        json={
            'year': '1973',
            'title': 'Café da manha dos campeões',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'year': '1973',
        'title': 'Café da manha dos campeões',
        'id': 1,
    }


def test_create_conflict(client, book_in_the_db):
    response = client.post(
        '/book/',
        json={
            'year': '1973',
            'title': 'Café da manha dos campeões',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Livro já possui registro'}


def test_read_book(client, book_in_the_db):
    response = client.get('/book/1')

    assert response.status_code == HTTPStatus.OK


def test_read_book_not_found(client):
    response = client.get('/book/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não encontrado'}


def test_update_book_success(client, book_in_the_db):
    response = client.patch(
        f'/book/{book_in_the_db.id}',
        json={'title': 'Silo'},
    )

    assert response.status_code == HTTPStatus.OK


def test_update_book_not_found(client):
    response = client.patch(
        '/book/1',
        json={'title': 'Silo'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não encontrado'}


def test_update_book_integrity_error(client, book_in_the_db, book_2_in_the_db):
    response = client.patch(
        '/book/1',
        json={'title': 'O ladrão de casaca'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Esse titulo já existe'}
