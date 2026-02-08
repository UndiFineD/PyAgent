# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_volweb.py\evidences.py\serializers_e678e772130a.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VolWeb\evidences\serializers.py

from evidences.models import Evidence

from rest_framework import serializers


class EvidenceSerializer(serializers.ModelSerializer):
    """

    Evidence Serializer

    Used to send json data to the front end for an evidence.

    """

    dump_linked_case_name = serializers.SerializerMethodField()

    class Meta:
        model = Evidence

        fields = "__all__"

        extra_fields = ["dump_linked_case_name"]

    def get_dump_linked_case_name(self, obj):

        # Return the name of the linked case instead of the id

        return obj.dump_linked_case.case_name


class AnalysisStartSerializer(serializers.Serializer):
    dump_id = serializers.IntegerField()
