from app import create_app
import json, secrets, names
from random import randint

test_client = create_app().test_client()

# Token
def register_user():
    post_dict = {
        "name": names.get_first_name(),
        "last_name": names.get_last_name(),
        "email":f"{names.get_first_name()}@{names.get_last_name()}.com",
        "cpf":f"{randint(100, 999)}.{randint(100, 999)}.{randint(100, 999)}-{randint(10, 99)}",
        "genre":'male',
        "cellphone":f"({randint(10, 99)}) {randint(1000, 9999)}-{randint(1000, 9999)}",
        "password": "12345678",
        "birthdate":"01/01/01",
    }
    
    register_response = test_client.post(
        '/register',
        data=json.dumps(post_dict),
        content_type='application/json',
    )

    if register_response.status_code == 409:
        register_user()
    
    login_dict = {
        "email":post_dict['email'],
        "password": post_dict['password'],
    }

    return login_dict

def get_user_token():

    login_dict = register_user()

    response = test_client.post(
        '/login',
        data=json.dumps(login_dict),
        content_type='application/json',
    )

    return {'token': {'Authorization':f"Bearer {json.loads(response.get_data())['access_token']}"}}

def delete_user_with_token(token):
    test_client.delete('/user', headers=token)


# Adress GET
def test_if_adresses_route_accepts_GET_request():
    response = test_client.options('/adress').headers['Allow']

    assert 'GET' in response, "Method not allowed."
    

def test_if_GET_request_in_adresses_route_return_status_code_OK():
    token = get_user_token()['token']

    response = test_client.get('/adress', headers=token)

    delete_user_with_token(token)

    assert response.status_code == 200, "Incorrect status."


# Adress POST
def test_adress_route_accepts_POST_request():
    assert 'POST' in (test_client.options('/adress').headers['Allow']), "Method not allowed."

def test_if_POST_request_in_adress_route_return_status_code_CREATED():
    token = get_user_token()['token']

    post_dict = {
        "street": secrets.token_hex(10),
        "house_number": 1,
        "district": secrets.token_hex(10),
        "city": secrets.token_hex(10),
        "state": secrets.token_hex(10),
        "cep": "00000-000",
    }
    
    response = test_client.post(
        '/adress',
        data=json.dumps(post_dict),
        headers=token,
        content_type='application/json'
    )

    delete_user_with_token(token)

    assert response.status_code == 201, "Incorrect status."


# Adress PATCH
def test_adress_route_accepts_PATCH_request_by_id():
    assert 'PATCH' in (test_client.options('/adress/10').headers['Allow']), "Method not allowed."

def test_if_PATCH_request_by_id_in_adress_route_return_status_code_OK():
    token = get_user_token()['token']

    post_dict = {
        "street": secrets.token_hex(10),
        "house_number": 1,
        "district": secrets.token_hex(10),
        "city": secrets.token_hex(10),
        "state": secrets.token_hex(10),
        "cep": "00000-000",
    }
    
    post_response = test_client.post(
        '/adress',
        data=json.dumps(post_dict),
        headers=token,
        content_type='application/json'
    )

    post_data = json.loads(post_response.get_data())

    response = test_client.patch(
        f"/adress/{post_data['adress_id']}",
        data=json.dumps(post_dict),
        headers=token,
        content_type='application/json'
    )

    delete_user_with_token(token)

    assert response.status_code == 200, "Incorrect status."


# Adress DELETE
def test_adress_route_accepts_delete_by_id():
    assert 'DELETE' in (test_client.options('/adress/10').headers['Allow']), "Method not allowed."

def test_if_DELETE_request_by_id_in_adress_route_return_status_code_NOCONTENT():
    token = get_user_token()['token']

    post_dict = {
        "street": secrets.token_hex(10),
        "house_number": 1,
        "district": secrets.token_hex(10),
        "city": secrets.token_hex(10),
        "state": secrets.token_hex(10),
        "cep": "00000-000",
    }
    
    post_response = test_client.post(
        '/adress',
        data=json.dumps(post_dict),
        headers=token,
        content_type='application/json'
    )

    post_data = json.loads(post_response.get_data())

    response = test_client.delete(f"/adress/{post_data['adress_id']}", headers=token)

    assert response.status_code == 204, "Incorrect status."

def test_if_DELETE_request_by_id_in_adress_route_for_a_nonexistent_adress_id_return_status_code_NOTFOUND():
    response = test_client.delete(f"/adress/{float('inf')}")

    assert response.status_code == 404, "incorrect status."