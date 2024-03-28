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


    # Assuming you want to get scores from two different models, GPT-3.5 and GPT-4
    try:
        response_3_5 = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Analyze the following text for its readability and provide scores for standard readability tests like the SMOG Index, Flesch-Kincaid Grade Level, Coleman-Liau Index, and Gunning Fog Index. The output should be in the following json format: {{'smog_index': 3.5,'flesch_kincaid_grade': 2.5,'coleman_liau_index':3.5,'gunning_fog':2.5}}"
                },
                {
                    "role": "user",
                    "content": text,
                }
            ],
            max_tokens=256
        )
        """
        response_4 = openai.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {
                    "role": "system",
                    "content": "Analyze the following text for its readability and provide scores for standard readability tests like the SMOG Index, Flesch-Kincaid Grade Level, Coleman-Liau Index, and Gunning Fog Index. The output should be in the following json format: {{'smog_index': 3.5,'flesch_kincaid_grade': 2.5,'coleman_liau_index':3.5,'gunning_fog':2.5}}"
                },
                {
                    "role": "user",
                    "content": text,
                }
            ],
            max_tokens=256
        )
        """
        # Fetch the submission instance
        submission = TextSubmission.objects.get(id=submission_id)

        for test, score in json.loads(response_3_5.choices[0].message.content).items():
            # Update the submission with new scores
            submission.readability_scores[test].append({
                'score': score,
                'source': 'OpenAI GPT-3.5 Turbo',
                'usage': {'completion_tokens': response_3_5.usage.completion_tokens,
                          'prompt_tokens': response_3_5.usage.prompt_tokens,
                          'total_tokens': response_3_5.usage.total_tokens,
                          },
            })
        """
        for test, score in json.loads(response_4.choices[0].message.content).items():
            # Update the submission with new scores
            submission.readability_scores[test].append({
                'score': score,
                'source': 'OpenAI GPT-4 Turbo',
                'usage': {'completion_tokens': response_4.usage.completion_tokens,
                          'prompt_tokens': response_4.usage.prompt_tokens,
                          'total_tokens': response_4.usage.total_tokens,
                          },
            })
        """
        print(submission.readability_scores)

        # Save the updated submission
        submission.save()
        logger.info("Task completed for submission: %s", submission_id)

    except Exception as e:
        # Handle exceptions (e.g., API errors, submission not found)
        print(f"Error in fetching OpenAI scores: {e}")