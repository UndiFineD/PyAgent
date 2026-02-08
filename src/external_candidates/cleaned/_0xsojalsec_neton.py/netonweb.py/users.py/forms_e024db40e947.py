# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Neton\NetonWeb\users\forms.py
from django import forms


class AuthenticationForm(forms.Form):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={"class": "input"}),
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "input", "type": "password"}))
