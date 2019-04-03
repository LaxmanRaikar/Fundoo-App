from django.contrib.auth.models import User
import os
import pytest
from tests import client

testing=pytest.mark.django_db



def test_login():
    user=User.objects.create(username='lucky', password='123456789hi')
    responce = client.post( 'http://127.0.0.1:8000/api/login', {'username': 'lucky', 'password': '123456789hi'})