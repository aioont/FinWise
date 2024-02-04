from django.db import models
from django.contrib.auth.models import User

class LearningPath(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    financial_goals = models.TextField()
    current_knowledge = models.TextField()
    interests = models.TextField()
    suggested_modules = models.ManyToManyField('Module', related_name='learning_paths', blank=True)

    def __str__(self):
        return f'Learning Path for {self.user.username}'

class Module(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='article_images/')  # Assuming you have an 'article_images' folder in your MEDIA_ROOT

    def __str__(self):
        return self.title
