from django import forms

# TODO see if any other options for this form or any validation/cleaning needed
# TODO maybe add other slider options for the user to select in this
class TextInputForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)