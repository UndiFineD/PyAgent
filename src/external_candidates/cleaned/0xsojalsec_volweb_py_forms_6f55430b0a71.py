# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_volweb.py\cases.py\forms_6f55430b0a71.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VolWeb\cases\forms.py

from cases.models import Case

from django import forms

from django.forms import SelectMultiple, Textarea, TextInput


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case

        fields = ["case_name", "case_description", "linked_users"]

        widgets = {
            "case_name": TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "type": "text",
                    "required": "",
                }
            ),
            "case_description": Textarea(
                attrs={
                    "class": "form-control form-control-sm",
                    "rows": "4",
                    "required": "",
                }
            ),
            "linked_users": SelectMultiple(attrs={"class": "form-control form-control-sm"}),
        }
