from django.db import models

# Create your models here.
from django.db import models

class Poll(models.Model):
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.question
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.choice_text
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
