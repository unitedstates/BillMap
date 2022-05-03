from django import forms
from feedback.models import Feedback


class FeedbackModelForm(forms.ModelForm):
    content = forms.CharField(initial='', widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=1000)

    class Meta:
        model = Feedback
        fields = "__all__"
