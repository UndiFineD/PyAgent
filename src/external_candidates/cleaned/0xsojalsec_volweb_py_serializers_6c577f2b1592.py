# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_volweb.py\main.py\serializers_6c577f2b1592.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VolWeb\main\serializers.py

from main.models import Indicator

from rest_framework import serializers


class IndicatorSerializer(serializers.ModelSerializer):
    dump_linked_dump_name = serializers.SerializerMethodField()

    class Meta:
        model = Indicator

        fields = "__all__"

        extra_fields = ["dump_linked_dump_name"]

    def get_dump_linked_dump_name(self, obj):
        # Return the name of the linked case instead of the id

        return obj.evidence.dump_name
