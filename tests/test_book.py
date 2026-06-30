from http import HTTPStatus


def test_create_book(client):
    response = client.post(
        '/book/',
        json={
            'year': '1992',
            'title': 'Café da manha de campeões',
        }
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'year': '1992',
        'title': 'Café da manha de campeões',
        'id': 1
    }
