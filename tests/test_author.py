from http import HTTPStatus


def test_create_author(client, token):
    response = client.post(
        '/author/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'Kurt Vonnegut',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'name': 'Kurt Vonnegut',
        'id': 1,
    }


def test_create_author_conflict(client, author_in_the_db, token):
    response = client.post(
        '/author/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'Kurt Vonnegut',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Author já consta no MADR'}


def test_read_author(client, author_in_the_db, token):
    response = client.get(
        '/author/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'name': 'Kurt Vonnegut',
        'id': 1,
    }


def test_read_author_not_found(client, token):
    response = client.get(
        '/author/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author não consta no MADR'}


def test_update_author_success(client, author_in_the_db, token):
    response = client.patch(
        f'/author/{author_in_the_db.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Vonneg Jr'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'name': author_in_the_db.name,
        'id': author_in_the_db.id,
    }


def test_update_integrity_error(
    client, author_in_the_db, author_2_in_the_db, token
):
    response = client.patch(
        f'/author/{author_2_in_the_db.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Kurt Vonnegut'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Author já consta no MADR'}


def test_update_author_not_found(client, token):
    response = client.patch(
        '/author/1',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Vonneg Jr'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author não consta no MADR'}


def test_delete_author_success(client, author_in_the_db, token):
    response = client.delete(
        f'/author/{author_in_the_db.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'mensagem': 'Author deletado do MADR'}


def test_delete_author_not_found(client, author_in_the_db, token):
    response = client.delete(
        '/author/3',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Author não consta no MADR'}
