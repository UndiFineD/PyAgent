# Extracted from: C:\DEV\PyAgent\.external\coqui-ai-TTS\recipes\bel-alex73\dump_config.py
import json
import re

from train_glowtts import config

s = json.dumps(config, default=vars, indent=2)
s = re.sub(r'"test_sentences":\s*\[\],', "", s)
print(s)
