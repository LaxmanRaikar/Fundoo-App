import pytest

from django.urls import reverse
from rest_framework.test import APITestCase

class TestCases(APITestCase):

    @pytest.mark.django_db
    # def test_can_get_product_list(self):
    def test_registration(self):
        """test case for successful registration"""

        url = reverse('registerapi')
        print("mypath", url)

        user_data = {
            "username": "lucky",
            "email": "kiranraikar777@gmail.com",
            "password": "123456789hi",
        }
        response = self.client.post(url, user_data)
        z = response.json()['success']
        self.assertEqual(z, True)