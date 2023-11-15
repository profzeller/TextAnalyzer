from django.shortcuts import render
from .forms import TextSubmissionForm
from .models import TextSubmission, ReadabilityTestInfo
import textstat
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404


def submission_detail(request, pk):
    submission = get_object_or_404(TextSubmission, pk=pk)
    readability_tests = ReadabilityTestInfo.objects.all()

    return render(request, 'submission/submission_detail.html', {
        'submission': submission,
        'readability_tests': readability_tests
    })


def submit_text(request):
    if request.method == 'POST':
        form = TextSubmissionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            submission_text = form.cleaned_data['submission_text']
            word_count = len(submission_text.split())

            # Create TextSubmission instance
            submission = TextSubmission(title=title, submission_text=submission_text, word_count=word_count)

            # Calculate readability scores
            submission.flesch_reading_ease = textstat.flesch_reading_ease(submission_text)
            submission.smog_index = textstat.smog_index(submission_text)
            submission.flesch_kincaid_grade = textstat.flesch_kincaid_grade(submission_text)
            submission.coleman_liau_index = textstat.coleman_liau_index(submission_text)
            submission.automated_readability_index = textstat.automated_readability_index(submission_text)
            submission.dale_chall_readability_score = textstat.dale_chall_readability_score(submission_text)
            submission.difficult_words = textstat.difficult_words(submission_text)
            submission.linsear_write_formula = textstat.linsear_write_formula(submission_text)
            submission.gunning_fog = textstat.gunning_fog(submission_text)
            submission.text_standard = textstat.text_standard(submission_text, float_output=False)

            submission.save()

            # Redirect or show success message
            # ...

    else:
        form = TextSubmissionForm()

    return render(request, 'submission/submit_text.html', {'form': form})


def index(request):
    submissions = TextSubmission.objects.all()
    return render(request, 'submission/index.html', {'submissions': submissions})



