import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin


class Question(models.Model):
    """
    Represents a question in the poll.

    Attributes:
        question_text (str) : Field for text of the question.
        pub_date (datetime) : Field for the publication date.
        end_date (datetime) : Field for the end date of poll question.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    end_date = models.DateTimeField('date ended', default=None, null=True,
                                    blank=True)

    def __str__(self):
        """ Return a text of the question. """
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        """
        Checks if the poll question was published within last day.

        Return :
            bool: True if the question was published within last day.
            False otherwise.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Is published?',
    )
    def is_published(self):
        """
        Checks if the poll question is published.

        Return :
            bool: True if the current date is on or after poll question’s
            publication date. False otherwise.
        """
        now = timezone.now()
        return now >= self.pub_date

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Can vote?',
    )
    def can_vote(self):
        """
        Checks if the poll question can vote.

        Return :
            bool: True if voting is allowed for this poll question.
            False otherwise.
        """
        now = timezone.now()
        if self.end_date is None:
            return now >= self.pub_date
        return self.pub_date <= now <= self.end_date


class Choice(models.Model):
    """ Represents a choice in the poll question.

    Attribute:
        question (Question) : Foreign key to associate each choice
        with a question.
        choice_tex (str) : Field for text of the choice.
        votes (int) : Field for vote tally.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """ Return a text of the choice. """
        return self.choice_text
