from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'non.existing@mail.com'})

    assert response.status_code == 404
    assert response.json()['detail'] == "User not found"

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user_data = {
        'name': 'Sergey Simonov',
        'email': 's.e.simonov@mail.com'
    }
    response = client.post("/api/v1/user", json=new_user_data)
    assert response.status_code == 201
    assert isinstance(response.json(), int)

    # Дополнительно можно проверить, что пользователь действительно создался
    response_get = client.get("/api/v1/user", params={'email': new_user_data['email']})
    assert response_get.status_code == 200
    assert response_get.json()['email'] == new_user_data['email']

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    existing_email = users[0]['email']
    new_user_data = {
        'name': 'Another Ivanov',
        'email': existing_email
    }
    response = client.post("/api/v1/user", json=new_user_data)
    assert response.status_code == 409
    assert response.json()['detail'] == "User with this email already exists"

def test_delete_user():
    '''Удаление пользователя'''
    # Сначала создадим пользователя для теста удаления
    test_email = "to.delete@mail.com"
    client.post("/api/v1/user", json={'name': 'To Delete', 'email': test_email})
    
    # Удаляем пользователя
    response = client.delete("/api/v1/user", params={'email': test_email})
    assert response.status_code == 204
    
    # Проверяем, что пользователь действительно удалён
    response_get = client.get("/api/v1/user", params={'email': test_email})
    assert response_get.status_code == 404