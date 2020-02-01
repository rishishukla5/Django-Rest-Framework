from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Merchant(models.Model):
    name = models.CharField(max_length=50)
    merchant_id = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    website = models.URLField(verbose_name='Website Link', null=False)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
