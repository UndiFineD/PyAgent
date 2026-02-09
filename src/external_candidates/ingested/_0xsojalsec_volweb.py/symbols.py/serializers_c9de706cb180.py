# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VolWeb\symbols\serializers.py
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from rest_framework import serializers
from symbols.models import Symbol


class SymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symbol
        fields = "__all__"


@receiver(post_save, sender=Symbol)
def send_symbol_created(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    serializer = SymbolSerializer(instance)
    async_to_sync(channel_layer.group_send)(
        "symbols",
        {"type": "send_notification", "status": "created", "message": serializer.data},
    )


@receiver(post_delete, sender=Symbol)
def send_symbol_created(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    serializer = SymbolSerializer(instance)
    async_to_sync(channel_layer.group_send)(
        "symbols",
        {"type": "send_notification", "status": "deleted", "message": serializer.data},
    )
