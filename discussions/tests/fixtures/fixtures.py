import pytest
from rest_framework.test import APIClient

from discussions.models import User, Discussion, Comment


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def example_user(make_user):
    return make_user("example_user")


@pytest.fixture
def make_user(db):
    def make(user_name):
        return User.objects.create(username=user_name)

    return make


@pytest.fixture
def make_discussion(db):
    def make(user, title):
        return Discussion.objects.create(
            creator=user,
            title=title
        )

    return make


@pytest.fixture
def example_discussion(make_discussion, example_user):
    return make_discussion(example_user, "This is a discussion example title")


@pytest.fixture
def another_user(make_user):
    return make_user("another_user")


@pytest.fixture
def make_comment(db):
    def make(author, discussion, content, parent=None):
        return Comment.objects.create(
            author=author,
            discussion=discussion,
            content=content,
            parent=parent
        )
    return make


@pytest.fixture
def example_comment(make_comment, example_user, example_discussion):
    return make_comment(example_user, example_discussion, "This is an example comment")


@pytest.fixture
def example_reply(make_comment, another_user, example_discussion, example_comment):
    return make_comment(another_user, example_discussion, "This is a reply", parent=example_comment)
