from django import forms


# Note that it is not inheriting from forms.ModelForm
class QueryForm(forms.Form):
    auto_id = False
    queryText = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "rows": 8,
                "class": "form-control",
                "placeholder": "Enter text for bills or resolutions"
            }
        )
    )
