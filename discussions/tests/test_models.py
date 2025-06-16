from discussions.models import Comment


class TestDiscussionModel:
    def test_comment_creation(self, example_user, example_discussion):
        comment1 = Comment.objects.create(
            discussion=example_discussion,
            author=example_user,
            content="Top Comment"
        )

        assert comment1.content == "Top Comment"
        assert comment1.author.username == "example_user"
        assert comment1.discussion.title == "This is a discussion example title"
