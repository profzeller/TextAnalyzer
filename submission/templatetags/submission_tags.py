from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
def get_test_score(submission, test_name):
    """Retrieve the test score from a submission based on the test name."""
    try:
        # Use 'getattr' to dynamically get the attribute based on test_name
        return getattr(submission, test_name, "Not available")
    except AttributeError:
        return "Not available"
