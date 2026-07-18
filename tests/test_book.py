from http import HTTPStatus


def test_create_book(client):
    response = client.post(
        '/book/',
        json={
            'year': '1992',
            'title': 'Café da manha de campeões',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'year': '1992',
        'title': 'Café da manha de campeões',
        'id': 1,
    }


def test_create_conflict(client, book_in_the_db):
    response = client.post(
        '/book/',
        json={
            'year': '1992',
            'title': 'Café da manha de campeões',
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
