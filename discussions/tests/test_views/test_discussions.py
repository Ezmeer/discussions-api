import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from discussions.models import Discussion


@pytest.mark.django_db
class TestDiscussionsViewSet:

    def setup_method(self):
        self.client = APIClient()

    def test_list_discussions(self, example_discussion, another_user, make_discussion):
        make_discussion(another_user, "Second discussion")

        url = reverse('discussions-list')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2
        assert response.data['results'][0]['title'] == "Second discussion"
        assert response.data['results'][1]['title'] == "This is a discussion example title"

    def test_retrieve_discussion(self, example_discussion):
        url = reverse('discussions-detail', kwargs={'pk': example_discussion.id})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == "This is a discussion example title"
        assert response.data['id'] == example_discussion.id

    def test_create_discussion(self, example_user):
        url = reverse('discussions-list')
        data = {
            'creator': example_user.id,
            'title': 'New Discussion Title'
        }
        response = self.client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'New Discussion Title'
        assert Discussion.objects.filter(title='New Discussion Title').exists()

    def test_delete_discussion_success(self, example_discussion, example_user):
        url = reverse('discussions-delete-discussion', kwargs={'pk': example_discussion.id})
        data = {'creator': example_user.id}
        response = self.client.post(url, data)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Discussion.objects.filter(id=example_discussion.id).exists()

    def test_delete_discussion_wrong_owner(self, example_discussion, another_user):
        url = reverse('discussions-delete-discussion', kwargs={'pk': example_discussion.id})
        data = {'creator': another_user.id}
        response = self.client.post(url, data)

        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST]
        assert Discussion.objects.filter(id=example_discussion.id).exists()

    def test_update_title_success(self, example_discussion, example_user):
        url = reverse('discussions-update-title', kwargs={'pk': example_discussion.id})
        data = {
            'creator': example_user.id,
            'title': 'Updated Discussion Title'
        }
        response = self.client.post(url, data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Discussion Title'

        example_discussion.refresh_from_db()
        assert example_discussion.title == 'Updated Discussion Title'

    def test_update_title_wrong_owner(self, example_discussion, another_user):
        original_title = example_discussion.title
        url = reverse('discussions-update-title', kwargs={'pk': example_discussion.id})
        data = {
            'creator': another_user.id,
            'title': 'Updated Discussion Title'
        }
        response = self.client.post(url, data)

        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST]

        example_discussion.refresh_from_db()
        assert example_discussion.title == original_title
