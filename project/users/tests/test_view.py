from project.users.models import User
import pytest
import json
# from rest_framework.test import APITestCase
from rest_framework.test import APIClient


#TESTING FOR  USER SIGNUP   
@pytest.mark.django_db
def test_user_signup(client,user_data):
    headers = {
            "Content-Type": "application/json",
            "Accept":"*/*"
        }
    assert User.objects.count() == 0
    resp = client.post("/auth/users/", data=user_data, headers=headers)
    print(resp.json())
    assert User.objects.count() == 1
    assert resp.status_code == 201


#TESTING FOR  USER LOGIN   
# @pytest.mark.django_db
# def test_default_user_login(client, create_test_user, user_data):
#     headers = {
#             "Content-Type": "application/json;charset=UTF-8"
#         }
#     body = {"username":"sodiqb86@gmail.com","password":"BAlogunSodiq134#@"}
#     assert User.objects.count() == 1
#     resp = client.post('/api-token-auth/', data = body, headers=headers)
#     token = resp.json()['token']
#     print(token)
#     assert resp.status_code == 200


#TESTING API FOR CREATING PRODUCT,SERVICES AND EVENT
@pytest.mark.django_db
def test_what_to_sell(client,create_test_user,create_what_to_sell):
    client = APIClient()
    client.force_authenticate(create_test_user)
    resp = client.post('/services', data = create_what_to_sell, format='json')
    assert resp.status_code == 200

#TESTING API FOR GETTING ALL PRODUCT,SERVICES AND EVENT
@pytest.mark.django_db
def test_explore(client,create_test_user,create_what_to_sell):
    client = APIClient()
    client.force_authenticate(create_test_user)
    client.post('/services', data = create_what_to_sell, format='json')
    resp = client.get('/explore')
    assert resp.status_code == 200
    
#TESTING API FOR GETTING  PRODUCT,SERVICES AND EVENT BASE ON TAG INPUT
@pytest.mark.django_db
def test_explore_by_tag(client,create_test_user,create_what_to_sell):
    client = APIClient()
    client.force_authenticate(create_test_user)
    client.post('/services', data = create_what_to_sell, format='json')
    resp = client.post('/explore', data={"input_tag":"phone"},format = 'json')
    assert resp.status_code == 200
    
#TESTING API FOR GETTING  PRODUCT,SERVICES AND EVENT DETAILS
@pytest.mark.django_db
def test_explore_detail(client,create_test_user,create_what_to_sell):
    client = APIClient()
    client.force_authenticate(create_test_user)
    client.post('/services', data = create_what_to_sell, format='json')
    resp = client.post('/explore_detail', data={"title":"phone","id":1},format = 'json')
    print(resp.json())
    assert resp.status_code == 200
    
#TESTING API FOR GETTING ALL PRODUCT,SERVICES AND EVENT FOR ONLY USER
@pytest.mark.django_db
def test_dashboard(client,create_test_user,create_what_to_sell):
    client = APIClient()
    client.force_authenticate(create_test_user)
    client.post('/services', data = create_what_to_sell, format='json')
    resp = client.get('/dashboard')
    assert resp.status_code == 200
    
#TESTING API FOR GETTING  PRODUCT,SERVICES AND EVENT BASE ON TAG INPUT FOR ONLY USER
@pytest.mark.django_db
def test_dashboard_by_tag(client,create_test_user,create_what_to_sell):
    client = APIClient()
    client.force_authenticate(create_test_user)
    client.post('/services', data = create_what_to_sell, format='json')
    resp = client.post('/dashboard', data={"input_tag":"phone"},format = 'json')
    assert resp.status_code == 200
    

#TESTING API FOR GETTING ALL INTERESTS
@pytest.mark.django_db
def test_get_all_interest(client):
    client = APIClient()
    resp = client.get('/interest')
    assert resp.status_code == 200

#TESTING API FOR GETTING USER PROFILE
@pytest.mark.django_db
def test_get_user_profile(client,create_test_user):
    client = APIClient()
    client.force_authenticate(create_test_user)
    resp = client.get('/user')
    assert resp.status_code == 200

#TESTING API FOR DELETING INTEREST_ID FROM USER INTEREST LIST
@pytest.mark.django_db
def test_delete_from_interest_list(client,create_test_user):
    client = APIClient()
    client.force_authenticate(create_test_user)
    resp = client.delete('/user',data = {"interestID":3}, format='json')
    assert resp.status_code == 200

#TESTING API FOR ADDING INTEREST_ID TO USER INTEREST LIST
@pytest.mark.django_db
def test_add_to_interest_list(client,create_test_user):
    client = APIClient()
    client.force_authenticate(create_test_user)
    resp = client.post('/user',data = {"interestID":4}, format='json')
    assert resp.status_code == 200
