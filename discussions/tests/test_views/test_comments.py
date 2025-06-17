import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from discussions.models import Comment


@pytest.mark.django_db
def test_create_comment(api_client, example_user, example_discussion):
    url = reverse("comments-list")
    data = {
        "author": example_user.id,
        "discussion": example_discussion.id,
        "content": "New comment"
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["content"] == "New comment"


@pytest.mark.django_db
def test_create_comment_missing_fields(api_client):
    url = reverse("comments-list")
    response = api_client.post(url, {})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_list_comments(api_client, example_comment):
    url = reverse("comments-list") + f"?discussion_id={example_comment.discussion.id}"
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert any(c["id"] == example_comment.id for c in response.data["results"])


@pytest.mark.django_db
def test_list_comments_missing_discussion_id(api_client):
    url = reverse("comments-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_retrieve_replies(api_client, example_reply):
    url = reverse("comments-replies", kwargs={"pk": example_reply.parent.id})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert any(r["id"] == example_reply.id for r in response.data["results"])


@pytest.mark.django_db
def test_update_comment(api_client, example_comment):
    url = reverse("comments-update-content", kwargs={"pk": example_comment.id})
    data = {
        "creator": example_comment.author.id,
        "content": "Updated content"
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["content"] == "Updated content"


@pytest.mark.django_db
def test_update_comment_forbidden(api_client, example_comment, another_user):
    url = reverse("comments-update-content", kwargs={"pk": example_comment.id})
    data = {
        "creator": another_user.id,
        "content": "Hacked update"
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_delete_comment(api_client, example_comment):
    url = reverse("comments-delete-comment", kwargs={"pk": example_comment.id})
    data = {"creator": example_comment.author.id}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Comment.objects.filter(id=example_comment.id).exists()


@pytest.mark.django_db
def test_delete_comment_forbidden(api_client, example_comment, another_user):
    url = reverse("comments-delete-comment", kwargs={"pk": example_comment.id})
    data = {"creator": another_user.id}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
