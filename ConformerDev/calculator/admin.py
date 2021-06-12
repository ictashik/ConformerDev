from django.contrib import admin

# Register your models here.
from calculator.models import Project,Error,Test

admin.site.register(Project)
admin.site.register(Error)
admin.site.register(Test)
