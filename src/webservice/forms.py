from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    wikitext = forms.CharField(max_length=4000, required=False)
    date = forms.CharField(max_length=32, required=False)
    author = forms.CharField(max_length=64, required=False)
    latitude = forms.CharField(max_length=16, required=False)
    longitude = forms.CharField(max_length=16, required=False)
    categories = forms.CharField(max_length=1000, required=False)
    file = forms.FileField()

class OauthDoneForm(forms.Form):
    token=forms.CharField(label='Token', max_length=254)
    route=forms.CharField(label='Route', max_length=254)
    provider=forms.CharField(label='Provider', max_length=254)
