from django.db import models
from books.models import Book
from users.models import Profile
import uuid


class Review(models.Model):
    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile    = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True, default=None)
    book       = models.ForeignKey(Book, on_delete=models.PROTECT)
    content    = models.TextField()
    date_added = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.profile.user.first_name} {self.profile.user.last_name} ({self.profile.user.username})'s review on {self.book.title}"