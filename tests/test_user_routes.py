from app import create_app
import json

test_client = create_app().test_client()

# User POST
def test_register_user_route_accepts_POST_request():
    assert 'POST' in (test_client.options('/register').headers['Allow']), "Method not allowed."

def test_login_user_route_accepts_POST_request():
    assert 'POST' in (test_client.options('/login').headers['Allow']), "Method not allowed."

def test_if_REGISTER_request_in_users_route_return_status_code_CREATED():
    post_dict = {
        "name":"name_test",
        "last_name":"last_name_test",
        "email":"email_test@example.com",
        "cpf":"000.000.000-11",
        "genre":'male',
        "cellphone":"(00) 00000-0000",
        "password": "12345678",
        "birthdate":"01/01/01",
    }
    
    response = test_client.post(
        '/register',
        data=json.dumps(post_dict),
        content_type='application/json',
    )

    assert response.status_code == 201, "Incorrect status."
def pytest_namespace():
    return {'authorization_token': ''}

def test_if_LOGIN_request_in_users_route_return_status_code_CREATED():
    post_dict = {
        "email":"email_test@example.com",
        "password": "12345678",
    }

    response = test_client.post(
        '/login',
        data=json.dumps(post_dict),
        content_type='application/json',
    )
    response_data = json.loads(response.get_data())
    pytest_namespace.authorization_token = response_data['access_token']

    assert response.status_code == 200, "Incorrect status."

# User GET
def test_user_route_accepts_GET_request():
    assert 'GET' in (test_client.options('/user').headers['Allow']), "Method not allowed."

def test_if_GET_request_in_user_route_return_status_code_OK():
    headers = {
        'Authorization': 'Bearer {}'.format(pytest_namespace.authorization_token)
    }
    response = test_client.get(
        '/user',
        headers=headers        
    )
    assert response.status_code == 200, "Incorrect status."	

# User PATCH
def test_user_route_accepts_PATCH_request():
    assert 'PATCH' in (test_client.options('/user').headers['Allow']), "Method not allowed."

def test_if_PATCH_request_in_user_route_return_status_code_OK():
    update_dict = {
        "last_name": "last_name_test_patch",
    }
    headers = {
        'Authorization': 'Bearer {}'.format(pytest_namespace.authorization_token)
    }

    response = test_client.patch(
        '/user',
        headers=headers,
        data=json.dumps(update_dict),
        content_type='application/json',
    )

    assert response.status_code == 200, "Incorrect status."	

# User DELETE
def test_user_route_accepts_DELETE_request():
    assert 'DELETE' in (test_client.options('/user').headers['Allow']), "Method not allowed."

def test_if_DELETE_request_in_user_route_return_status_code_NO_CONTENT():
    headers = {
        'Authorization': 'Bearer {}'.format(pytest_namespace.authorization_token)
    }

    response = test_client.delete(
        '/user',
        headers=headers,
    )

    assert response.status_code == 204, "Incorrect status."	