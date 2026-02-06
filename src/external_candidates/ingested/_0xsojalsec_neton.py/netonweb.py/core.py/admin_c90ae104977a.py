# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Neton\NetonWeb\core\admin.py
from django.contrib import admin

from .models import Checksandbox, Execution, Filecrawler, Hook, Systeminfo, Targets

admin.site.register(Targets)
admin.site.register(Execution)
admin.site.register(Hook)
admin.site.register(Checksandbox)
admin.site.register(Filecrawler)
admin.site.register(Systeminfo)
