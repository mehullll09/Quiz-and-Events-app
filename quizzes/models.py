from django.db import models
from django.utils import timezone

# Create your models here.

class Quiz(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Questions(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(max_length=100, default='MCQ')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.text


class Answers(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class UserSubmission(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    score = models.IntegerField()
    submitted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user_name


class UserAnswer(models.Model):
    submission = models.ForeignKey(UserSubmission, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answers, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.submission} - {self.question}"