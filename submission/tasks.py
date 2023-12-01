from celery import shared_task
import openai
from django.conf import settings
from .models import TextSubmission
import json
import logging

logger = logging.getLogger(__name__)

@shared_task
def fetch_openai_scores(submission_id, text):
    # Set the OpenAI API key
    logger.info("Task started for submission: %s", submission_id)
    openai.api_key = settings.OPENAI_API_KEY

    prompt = f"""

    Analyze the following text for its readability and provide scores for standard readability tests like the SMOG Index, Flesch-Kincaid Grade Level, Coleman-Liau Index, and Gunning Fog Index. The output should be in the following json format:

    {{
    'smog_index' = 3.5,
    'flesch_kincaid_grade' = 2.5,
    'coleman_liau_index' = 3.5,
    'gunning_fog' = 2.5
    }}
    
    Text: {text}
    """


    # Assuming you want to get scores from two different models, GPT-3.5 and GPT-4
    try:
        response_3_5 = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=50
        )
        # response_4 = openai.Completion.create(
        #     model="text-davinci-004",  # Replace with actual GPT-4 model name if different
        #     prompt=prompt,
        #     max_tokens=50
        # )

        # Fetch the submission instance
        submission = TextSubmission.objects.get(id=submission_id)

        for test, score in json.loads(response_3_5.choices[0].text).items():
            # Update the submission with new scores
            submission.readability_scores[test].append({
                'score': score,
                'source': 'OpenAI GPT-3.5 text-davinci-003'
            })
        # for test, score in json.loads(response_4.choices[0].text).items():
        #     submission.readability_scores[test].append({
        #         'score': score,
        #         'source': 'OpenAI GPT-4 text-davinci-004'
        #     })

        print(submission.readability_scores)

        # Save the updated submission
        submission.save()
        logger.info("Task completed for submission: %s", submission_id)

    except Exception as e:
        # Handle exceptions (e.g., API errors, submission not found)
        print(f"Error in fetching OpenAI scores: {e}")

@shared_task
def add(x, y):
    logger.info("Adding %d + %d", x, y)
    return x + y