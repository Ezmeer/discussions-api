from django.db import models


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"User id {self.id} and name: {self.username}"


class Discussion(TimeStamp):
    title = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        indexes = [models.Index(fields=['created_at'])]

    def __str__(self):
        return f"Discussion {self.id} by User {self.creator.username}"


class Comment(TimeStamp):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    content = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=['discussion']),
            models.Index(fields=['parent']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Comment {self.id} by User {self.user_id}"
