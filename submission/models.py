from django.db import models
from django.utils import timezone
from django.db.models import JSONField


class TextSubmission(models.Model):
    title = models.CharField(max_length=200)
    submission_text = models.TextField()
    word_count = models.IntegerField(default=0)
    submission_time = models.DateTimeField(default=timezone.now)



    # Fields for readability scores
    flesch_reading_ease = models.FloatField(null=True, blank=True)
    flesch_reading_ease = models.FloatField(null=True, blank=True)
    smog_index = models.FloatField(null=True, blank=True)
    flesch_kincaid_grade = models.FloatField(null=True, blank=True)
    coleman_liau_index = models.FloatField(null=True, blank=True)
    automated_readability_index = models.FloatField(null=True, blank=True)
    dale_chall_readability_score = models.FloatField(null=True, blank=True)
    difficult_words = models.IntegerField(null=True, blank=True)
    linsear_write_formula = models.FloatField(null=True, blank=True)
    gunning_fog = models.FloatField(null=True, blank=True)
    text_standard = models.CharField(max_length=100, null=True, blank=True)


class ReadabilityTestInfo(models.Model):
    test_name = models.CharField(max_length=100)  # This is the field name in your TextSubmission model
    display_name = models.CharField(max_length=100)  # A human-readable name for display purposes
    description = models.TextField()
    more_info_link = models.URLField()

    def __str__(self):
        return self.test_name

