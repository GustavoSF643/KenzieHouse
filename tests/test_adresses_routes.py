from app import create_app
import secrets
import json

test_client = create_app().test_client()

# Token
def get_user_token():
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

    return {'token': json.loads(response.get_data())['access_token']}

# Adresses GET
def test_if_adresses_route_accepts_GET_request():
    assert 'GET' in (test_client.options('/adresses').headers['Allow']), "Method not allowed."

def test_if_GET_request_in_adresses_route_return_status_code_OK():
    response = test_client.get('/adresses')

    assert response.status_code == 200, "Incorrect status."