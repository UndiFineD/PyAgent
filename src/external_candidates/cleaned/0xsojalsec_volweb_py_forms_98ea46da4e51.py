# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_volweb.py\evidences.py\forms_98ea46da4e51.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VolWeb\evidences\forms.py

from cases.models import Case

from django import forms

from django.forms import Select, TextInput

from evidences.models import Evidence


class EvidenceForm(forms.ModelForm):
    class Meta:
        model = Evidence

        fields = ["dump_name", "dump_os", "dump_linked_case"]

        dump_linked_case = forms.ModelChoiceField(queryset=Case.objects.all(), required=True)

        widgets = {
            "dump_name": TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "type": "text",
                    "required": "",
                }
            ),
            "dump_os": Select(
                attrs={
                    "value": "Windows",
                    "class": "form-select form-control form-control-sm",
                }
            ),
            "dump_linked_case": Select(attrs={"class": "form-select form-control form-control-sm "}),
        }
