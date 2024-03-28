from django.contrib import admin

# Register your models here.
from .models import TextSubmission, ReadabilityTestInfo

admin.site.register(TextSubmission)
admin.site.register(ReadabilityTestInfo)