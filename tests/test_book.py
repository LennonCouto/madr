from http import HTTPStatus


def test_create_book(client, author_in_the_db, token):
    response = client.post(
        '/book/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'year': '1973',
            'title': 'Café Da Manha Dos Campeões',
            'author_id': author_in_the_db.id,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'year': '1973',
        'title': 'Café Da Manha Dos Campeões',
        'author_id': author_in_the_db.id,
        'id': 1,
    }


def test_create_conflict(client, book_in_the_db, author_in_the_db, token):
    response = client.post(
        '/book/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'year': '1973',
            'title': 'Café Da Manha Dos Campeões',
            'author_id': author_in_the_db.id,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Livro já possui registro'}


def test_read_book(client, book_in_the_db, token):
    response = client.get(
        '/book/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK


def test_read_book_not_found(client, token):
    response = client.get(
        '/book/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não encontrado'}


def test_update_book_success(client, book_in_the_db, token):
    response = client.patch(
        f'/book/{book_in_the_db.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'Silo'},
    )

    assert response.status_code == HTTPStatus.OK


def test_update_book_not_found(client, token):
    response = client.patch(
        '/book/1',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'Silo'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não encontrado'}


def test_update_book_integrity_error(
    client, book_in_the_db, book_2_in_the_db, token
):
    response = client.patch(
        '/book/1',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'O ladrão de casaca'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Esse titulo já existe'}


def test_delete_book_success(client, book_in_the_db, token):
    response = client.delete(
        '/book/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'mensagem': 'Livro excluido da MADR'}


def test_delete_book_not_found(client, book_in_the_db, token):
    response = client.delete(
        '/book/2', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não encontrado'}
