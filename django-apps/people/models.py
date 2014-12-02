from django.db import models
from datetime import datetime

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=50)
    company = models.CharField(max_length=99)
    title = models.CharField(max_length=50, blank=True)
    sex = models.CharField(max_length=20, default="m")
    height = models.IntegerField(default=5)
    weight = models.IntegerField(default=5)
    skin = models.IntegerField(default=5)
    hair_color = models.CharField(max_length=20, blank=True)
    hair = models.CharField(max_length=99, blank=True)
    face = models.CharField(max_length=50, blank=True)
    extra = models.CharField(max_length=99, blank=True)
    def __str__(self):
        return "%s - %s" % (self.name, self.company)
    class Meta:
        ordering = ['name']

class Purpose(models.Model):
    description = models.CharField(max_length=30)
    def __str__(self):
        return self.description
    
class Interaction(models.Model):
    date = models.DateTimeField(default=datetime.now)
    person = models.ForeignKey(Person)
    purpose = models.ForeignKey(Purpose)
    details = models.CharField(max_length=200, blank=True)
    def __str__(self):
        return "%s %s, %s" % (self.date.strftime("%d/%m/%Y (%H:%M)"), self.person, self.purpose)
