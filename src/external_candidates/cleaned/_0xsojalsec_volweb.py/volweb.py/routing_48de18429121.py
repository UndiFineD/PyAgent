# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VolWeb\VolWeb\routing.py
from django.urls import path

from .consumers import (
    CasesTaskConsumer,
    EvidencesTaskConsumer,
    SymbolsTaskConsumer,
    VolatilityTaskConsumer,
)

websockets_urlpatterns = [
    path("ws/volatility_tasks/windows/<int:dump_id>/", VolatilityTaskConsumer.as_asgi()),
    path("ws/cases/", CasesTaskConsumer.as_asgi()),
    path("ws/evidences/", EvidencesTaskConsumer.as_asgi()),
    path("ws/symbols/", SymbolsTaskConsumer.as_asgi()),
]
