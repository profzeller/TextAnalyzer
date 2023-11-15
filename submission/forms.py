from django import forms


class TextSubmissionForm(forms.Form):
    title = forms.CharField(max_length=200)
    submission_text = forms.CharField(widget=forms.Textarea)
