from django.db import models
from django.urls import reverse

class AuthorPost(models.Model):
    name = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'pk': self.pk})

    def __str__(self):
        # return self.title 将文章标题返回
        return 'Name: ' + self.name