from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework import status

# 참고 lib: Python unittest => django.test.TestCase => rest_framework.test

# test 명령어가 실행되면 새로 생성된 테스트용 DB에 데이터가 저장된다. 게다가, 테스트 실행의 순서도 없다.


class UserRegistrationAPIViewTestCase(APITestCase):
    def test_registration(self):
        url = reverse("all_users")
        user_data = {
            "email": "user7@test.com",
            "password": "1234",
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 201)


class UserLoginAPIViewTestCase(APITestCase):
    def test_registration(self):
        url = reverse("token_obtain_pair")
        user_data = {
            "email": "user3@test.com",
            "password": "1234",
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 200)
