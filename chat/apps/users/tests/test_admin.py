import pytest
from django.urls import reverse

from ..models import User

pytestmark = pytest.mark.django_db


# noinspection PyProtectedMember
@pytest.fixture(autouse=True)
def admin_user(
    db: None, django_user_model, django_username_field: str
):  # pylint: disable=unused-argument
    UserModel = django_user_model

    try:
        user = User.objects.get(username="admin")
    except UserModel.DoesNotExist:
        user = User()
        user.username = "admin"
        user.set_password("password")

        user.first_connect = False
        user.is_superuser = True
        user.is_staff = True

        user.save()
    return user


class TestUserAdmin:
    def test_changelist(self, admin_client):
        url = reverse("admin:users_user_changelist")
        print(url)
        response = admin_client.get(url)
        assert response.status_code == 200

    def test_search(self, admin_client):
        url = reverse("admin:users_user_changelist")
        response = admin_client.get(url, data={"q": "test"})
        assert response.status_code == 200

    def test_add(self, admin_client):
        url = reverse("admin:users_user_add")
        response = admin_client.get(url)
        assert response.status_code == 200

        response = admin_client.post(
            url,
            data={
                "username": "test",
                "password1": "My_R@ndom-P@ssw0rd",
                "password2": "My_R@ndom-P@ssw0rd",
            },
        )
        assert response.status_code == 302
        assert User.objects.filter(username="test").exists()

    def test_view_user(self, admin_client):
        user = User.objects.get(username="admin")
        url = reverse("admin:users_user_change", kwargs={"object_id": user.pk})
        response = admin_client.get(url)
        assert response.status_code == 200
