from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Post
from users.models import CustomUser
from .serializers import PostSerializer

# ✅ 이미지 파일
from PIL import Image
import tempfile
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY

# ✅ Faker
from faker import Faker


def get_temp_image(temp_file):
    size = (320, 240)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, "png")
    return temp_file


class CreatePostTest(APITestCase):

    """
    @classmethod: 인스턴스 없이, 클래스 프로토타입만으로도 실행할 수 있는 메소드. 첫 번째 인자 값은, self 대신 cls를 사용한다. 클래스 스스로를 호출하는 것이 가능하다.

    @staticmethod: 사용 방법은 @classmethod와 같다. 클래스 바깥 스코프에 별도로 함수를 선언하는 것과 같은 역할을 한다. 깔끔한 코드, 일관성 있는 코드를 위해서 주로 작성한다.
    """

    """
    def setUp(self):
        # setUp 메소드 내 데이터들은 매 테스트 메소드가 실행될 때마다, 다시 실행된다. 만약 한 번만 실행하고, 다른 테스트 메소스들에 대해 같은 데이터를 사용하게 하고 싶을 때는, setUpTestData 메소드를 사용한다.
        self.user_data = {
            "email": "user@test.com",
            "password": "1234",
        }
        self.user = CustomUser.objects.create_user(
            self.data.get("email"),
            self.data.get("password"),
        )
        self.access_token = self.client.post(
            reverse("token_obtain_pair"), self.user_data).data["access"]

        self.post_data = {
            "title": "",
            "content": "",
        }
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.fake = Faker()

        cls.user_data = {
            "email": f"{cls.fake.first_name()}@test.com",
            "password": cls.fake.word(),
        }
        cls.user = CustomUser.objects.create_user(
            cls.user_data.get("email"),
            cls.user_data.get("password"),
        )

        cls.post_data = {
            "title": cls.fake.sentence(),
            "content": cls.fake.text(),
        }

        cls.posts = []

        for _ in range(5):
            post_data = {
                "title": cls.fake.sentence(),
                "content": cls.fake.text(),
            }
            post = Post.objects.create(
                user=cls.user,
                title=post_data.get("title"),
                content=post_data.get("content"),
            )
            cls.posts.append(post)

    def setUp(self) -> None:
        response = self.client.post(
            reverse("token_obtain_pair"), self.user_data)
        self.access_token = response.data["access"]

    def test_if_login_failed(self):
        # HTTP_AUTHORIZATION 데이터도 함께 보내야 정상적으로 동작한다.
        url = reverse("all_posts")
        response = self.client.post(url, self.post_data)

        # permission_classes 때문에 로그인 되어 있지 않으면, 401 에러를 반환. 아니면, views.py에서 지정한 대로 400 에러를 반환한다.
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    def test_create_post(self):
        response = self.client.post(
            path=reverse("all_posts"),
            data=self.post_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # ✅ 이미지 파일을 포함한 포스트 업로드
    def test_create_post_with_image(self):
        # 파이썬에서 제공하는 (이름 있는) 임시 파일 생성 방법
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name = "image.png"
        image_file = get_temp_image(temp_file)
        image_file.seek(0)
        self.post_data["photo"] = image_file

        # 전송
        response = self.client.post(
            path=reverse("all_posts"),
            data=encode_multipart(data=self.post_data, boundary=BOUNDARY),
            content_type=MULTIPART_CONTENT,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_post_detail(self):
        for post in self.posts:
            url = reverse("only_one_post", kwargs={"id": post.id})
            response = self.client.get(
                path=url,
            )
            serializer = PostSerializer(post)
            exclude_keys = ["like_users", "comments",]
            for key, value in serializer.data.items():
                if key not in exclude_keys:
                    self.assertEqual(response.data[key], value)

    def tearDown(self) -> None:
        return super().tearDown()
