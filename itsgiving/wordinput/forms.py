from django import forms

class MainForm(forms.Form):
    search_input = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'search-box-inner',
        })
    )

    university = forms.ChoiceField(
            choices=[
                ('oxford', 'Oxford'),
                ('cambridge', 'Cambridge')
            ],
            initial='cambridge'
        )
    
    undergrad_only = forms.BooleanField(
        initial=True,
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'undergrad-checkbox'
        })
    )