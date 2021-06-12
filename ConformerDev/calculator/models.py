from django.db import models

# Create your models here.
class Project(models.Model):
    title= models.CharField(max_length=300, unique=True)
    description= models.TextField()
    git_url= models.TextField()

class Test(models.Model):
    testID=models.IntegerField()
    userName = models.CharField(max_length=64)
    testFileURL = models.TextField()
    testDateTime = models.DateTimeField(auto_now_add=True)
    totalLines = models.TextField()
    AccessibilityExceptionCount = models.IntegerField()
    StaticHTMLValidationCount = models.IntegerField()


class Error(models.Model):
    testID = models.IntegerField(unique =False, null= True, blank = True)
    errorType = models.TextField()
    errorLocation = models.TextField()
    errorText = models.TextField()
