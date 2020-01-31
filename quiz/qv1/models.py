from django.db import models


# Create your models here.
class Quiz(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(verbose_name='description', null=True)
    created_date = models.DateField(auto_now=True)
    url = models.URLField(verbose_name='url', null=True)


class Question(models.Model):
    question = models.TextField(verbose_name='question', null=False)
    choice1 = models.TextField(verbose_name='choice1', null=False)
    choice2 = models.TextField(verbose_name='choice2', null=False)
    choice3 = models.TextField(verbose_name='choice3', null=False)
    choice4 = models.TextField(verbose_name='choice4', null=False)
    answer = models.CharField(max_length=10)
