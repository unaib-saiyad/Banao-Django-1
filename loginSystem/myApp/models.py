import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError


def get_uuid():
    while True:
        id = uuid.uuid4()
        if UserInformation.objects.filter(id=id).count() == 0:
            return id

def get_blog_uuid():
    while True:
        id = uuid.uuid4()
        if Blog.objects.filter(id=id).count() == 0:
            return id


TYPES = (
    ('Doctor', 'Doctor'),
    ('Patient', 'Patient'),
)

BLOG_CATEGORIES = (
    ('mental_health', 'mental_health'),
    ('nutrition', 'nutrition'),
    ('healthy_diet', 'healthy_diet'),
    ('obesity', 'obesity')
)


class UserInformation(models.Model):
    id = models.UUIDField(default=get_uuid, primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ImageField(upload_to='profile/', default='avatar.png')
    address = models.CharField(max_length=500, null=True, blank=True)
    type = models.CharField(max_length=20, default=TYPES[0], choices=TYPES, null=False, blank=False)

    def __str__(self):
        return str(self.user.username)


class Blog(models.Model):
    id = models.UUIDField(default=get_blog_uuid, primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=False, blank=False)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    category = models.CharField(max_length=100, choices=BLOG_CATEGORIES, null=False, blank=False)
    summary = models.TextField()
    content = models.TextField()
    draft = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    def save(self, *args, **kwargs):
        category_choices = [choice[0] for choice in BLOG_CATEGORIES]
        if self.category not in category_choices:
            raise ValidationError(f'{self.category} is not a valid category.')
        super(Blog, self).save(*args, **kwargs)
