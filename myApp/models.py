from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    name = models.CharField(max_length=100)
    # Add any other fields related to your game, such as start time, end time, etc.
    # You can also include fields for tracking game progress or difficulty levels.


class Sentence(models.Model):
    text = models.TextField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_valid = models.BooleanField(default=False)
    # Add any other fields specific to a sentence, such as timestamps or scores.


class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField()
    # Add any additional fields related to scoring, such as timestamps or leaderboard positions.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    valid_attempts = models.IntegerField(default=0)
    invalid_attempts = models.IntegerField(default=0)

    @property
    def total_attempts(self):
        return self.valid_attempts + self.invalid_attempts

    @property
    def valid_accuracy(self):
        if self.total_attempts > 0:
            return (self.valid_attempts / self.total_attempts) * 100
        return 0

    @property
    def invalid_accuracy(self):
        if self.total_attempts > 0:
            return (self.invalid_attempts / self.total_attempts) * 100
        return 0
