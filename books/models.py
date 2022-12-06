from django.db import models
import uuid
from users.models import Author
import uuid


class Book(models.Model):
    id      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ISBN    = models.CharField(max_length=100)
    title   = models.CharField(max_length=100)
    author  = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, null=True)
    summary = models.TextField()
    cover   = models.ImageField(default='default_book_cover.png', upload_to='book_cover_images')

    def __str__(self):
        return self.title
