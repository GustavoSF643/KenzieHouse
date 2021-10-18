from app import create_app
import secrets
import json

test_client = create_app().test_client()

# Categories GET
def test_categories_route_accepts_GET_request():
    assert 'GET' in (test_client.options('/categories').headers['Allow']), "Method not allowed."

def test_if_GET_request_in_categories_route_return_status_code_OK():
    response = test_client.get('/categories')

    assert response.status_code == 200, "Incorrect status."


# Categories POST
def test_categories_route_accepts_POST_request():
    assert 'POST' in (test_client.options('/categories').headers['Allow']), "Method not allowed."

def test_if_POST_request_in_categories_route_return_status_code_CREATED():
    post_dict = {
        "name": secrets.token_hex(10),
        "description": secrets.token_hex(16)
    }
    
    response = test_client.post(
        '/categories',
        data=json.dumps(post_dict),
        content_type='application/json'
    )

    response_data = json.loads(response.get_data())
    test_client.delete(f"/categories/{response_data['category_id']}")

    assert response.status_code == 201, "Incorrect status."


# Categories GET by id
def test_categories_route_accepts_GET_request_by_id():
    assert 'GET' in (test_client.options('/categories/10').headers['Allow']), "Method not allowed."

def test_if_GET_request_by_id_in_categories_route_return_status_code_OK():
    post_dict = {
        "name": secrets.token_hex(10),
        "description": secrets.token_hex(16)
    }
    
    post_response = test_client.post(
        '/categories',
        data=json.dumps(post_dict),
        content_type='application/json'
    )

    post_data = json.loads(post_response.get_data())

    response = test_client.get(f"/categories/{post_data['category_id']}")
    test_client.delete(f"/categories/{post_data['category_id']}")

    assert response.status_code == 200, "Incorrect status."

# Categories PATCH by id 
def test_categories_route_accepts_PATCH_request_by_id():
    assert 'PATCH' in (test_client.options('/categories/10').headers['Allow']), "Method not allowed."

def test_if_PATCH_request_by_id_in_categories_route_return_status_code_OK():
    post_dict = {
        "name": secrets.token_hex(10),
        "description": secrets.token_hex(16)
    }
    
    post_response = test_client.post(
        '/categories',
        data=json.dumps(post_dict),
        content_type='application/json'
    )

    post_data = json.loads(post_response.get_data())

    response = test_client.patch(
        f"/categories/{post_data['category_id']}",
        data=json.dumps(post_dict),
        content_type='application/json'
    )

    test_client.delete(f"/categories/{post_data['category_id']}")

    assert response.status_code == 200, "Incorrect status."

def test_if_PATCH_request_by_id_with_a_invalid_json_in_categories_route_return_status_code_NOTACCEPTABLE():
    post_dict = {
        "name": secrets.token_hex(10),
        "description": secrets.token_hex(16)
    }
    
    post_response = test_client.post(
        '/categories',
        data=json.dumps(post_dict),
        content_type='application/json'
    )

    post_data = json.loads(post_response.get_data())

    invalid_dicts = [
        {
            "abc": "a",
            "cba": "b"
        },
        {
            "name": 1,
            "description": 2
        },
        {
            "name": 1.0,
            "description": 2.0
        }
    ]
    status_code_list = []
    for invalid_dict in invalid_dicts:
        response = test_client.patch(
            f"/categories/{post_data['category_id']}",
            data=json.dumps(invalid_dict),
            content_type='application/json'
        )

        status_code_list.append(response.status_code)    

    test_client.delete(f"/categories/{post_data['category_id']}")

    for response in status_code_list:
        assert response == 406, "Incorrect status."


# Categories DELETE by id 
def test_categories_route_accepts_delete_by_id():
    assert 'DELETE' in (test_client.options('/categories/10').headers['Allow']), "Method not allowed."

def test_if_DELETE_request_by_id_in_categories_route_return_status_code_NOCONTENT():
    post_dict = {
        "name": secrets.token_hex(10),
        "description": secrets.token_hex(16)
    }
    
    post_response = test_client.post(
        '/categories',
        data=json.dumps(post_dict),
        content_type='application/json'
    )

    post_data = json.loads(post_response.get_data())

    response = test_client.delete(f"/categories/{post_data['category_id']}")

    assert response.status_code == 204, "Incorrect status."

def test_if_DELETE_request_by_id_in_categories_route_for_a_nonexistent_category_id_return_status_code_NOTFOUND():
    response = test_client.delete(f"/categories/{float('inf')}")

    assert response.status_code == 404, "incorrect status."