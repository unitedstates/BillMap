from django import forms

class QueryForm(forms.Form): #Note that it is not inheriting from forms.ModelForm
    auto_id = False
    queryText = forms.CharField(label="", widget=forms.Textarea(attrs={"rows":8, "cols":60, "placeholder":"Enter text from a bill section you want to search."}))
    #All my attributes here