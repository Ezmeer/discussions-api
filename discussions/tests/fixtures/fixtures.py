import pytest

from discussions.models import User, Discussion


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
