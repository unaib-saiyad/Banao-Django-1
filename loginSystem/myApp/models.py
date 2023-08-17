import uuid

from django.contrib.auth.models import User
from django.db import models


def get_uuid():
    while True:
        id = uuid.uuid4()
        if UserInformation.objects.filter(id=id).count() == 0:
            return id


TYPES = (
    ('Doctor', 'Doctor'),
    ('Patient', 'Patient'),
)


class UserInformation(models.Model):
    id = models.UUIDField(default=get_uuid, primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ImageField(upload_to='profile/', default='avatar.png')
    address = models.CharField(max_length=500, null=True, blank=True)
    type = models.CharField(max_length=20, default=TYPES[0], choices=TYPES, null=False, blank=False)

    def __str__(self):
        return str(self.user.username)
