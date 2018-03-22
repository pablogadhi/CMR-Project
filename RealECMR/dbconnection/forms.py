from django import forms
from django.db import connection

class QueryForm(forms.Form):
    query = forms.CharField(label='Query:', max_length=500,widget=forms.TextInput(attrs={'size':'120'}))

    def send(self):
        data = self.cleaned_data
        cursor = connection.cursor()
        cursor.execute(data.get("query"))
        return cursor.fetchall()
        # print(data.get("query"))

# class DummyForm(forms.Form):
