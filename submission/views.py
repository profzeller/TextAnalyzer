from django.shortcuts import render, redirect
from .forms import TextSubmissionForm
from .models import TextSubmission, ReadabilityTestInfo
import textstat
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404
from .tasks import fetch_openai_scores  # Assuming you have this task set up for Celery
from django.contrib.auth.decorators import login_required

@login_required
def submission_detail(request, pk):
    submission = get_object_or_404(TextSubmission, pk=pk)
    return render(request, 'submission/submission_detail.html', {
        'submission': submission,
    })

@login_required
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
            submission.readability_scores['smog_index'] = [{
                'score': textstat.smog_index(submission_text),
                'source': 'textstat'
            }]
            submission.readability_scores['flesch_kincaid_grade'] = [{
                'score': textstat.flesch_kincaid_grade(submission_text),
                'source': 'textstat'
            }]
            submission.readability_scores['coleman_liau_index'] = [{
                'score': textstat.coleman_liau_index(submission_text),
                'source': 'textstat'
            }]
            submission.readability_scores['gunning_fog'] = [{
                'score': textstat.gunning_fog(submission_text),
                'source': 'textstat'
            }]

            submission.save()

            # Asynchronously fetch scores from OpenAI (Celery task)
            fetch_openai_scores.delay(submission.id, submission.submission_text)

            # Redirect or show success message
            redirect('/submission/{}'.format(submission.id))

    else:
        form = TextSubmissionForm()

    return render(request, 'submission/submit_text.html', {'form': form})

@login_required
def index(request):
    submissions = TextSubmission.objects.all()
    return render(request, 'submission/index.html', {'submissions': submissions})



