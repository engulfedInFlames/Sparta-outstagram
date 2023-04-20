from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework import status

from .models import CustomUser

# 참고 lib: Python unittest => django.test.TestCase => rest_framework.test

# test 명령어가 실행되면 새로 생성된 테스트용 DB에 데이터가 저장된다. 게다가, 테스트 실행의 순서도 없다.

# 모든 테스트는 stateless해야 하며, 테스트 서로 간에 독립적이어야 한다. (그래서 초기화 된 DB를 사용한다.)

# 그렇다면 서로 의존 관계에 있는 서로 다른 테스트는 어떻게 실행시킬 수 있을까? setup(start)과 tearDown(end)을 사용하자.

# python, django, DRF 등의 빌트인 데이터가 아니라 사용자 정의한 데이터에 대해 테스트를 실행한다.


class LoginTest(APITestCase):
    def setUp(self):

        self.data = {
            "email": "user@test.com",
            "password": "1234",
        }
        self.user = CustomUser.objects.create_user(
            self.data.get("email"),
            self.data.get("password"),
        )
        self.access_token = self.client.post(
            reverse("token_obtain_pair"), self.data).data["access"]

    def test_login(self):
        url = reverse("token_obtain_pair")
        response = self.client.post(url, self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_detail(self):

        url = reverse("only_one_user", args=[self.user.id])
        response = self.client.get(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )

        self.assertEqual(response.data["email"],
                         self.data["email"],)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self) -> None:
        # tearDown은 setUp 과정에서 생성된 리소스를 cleanup한다.
        return super().tearDown()
