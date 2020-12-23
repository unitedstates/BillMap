from django import forms

class QueryForm(forms.Form): #Note that it is not inheriting from forms.ModelForm
    auto_id = False
    queryText = forms.CharField(label="", widget=forms.Textarea(attrs={"rows":8, "class":"form-control", "placeholder":"Enter text for bills or resolutions"}))
    #All my attributes here
