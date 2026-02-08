# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\tests\litellm-reasoning.py
from litellm import completion

messages = [{"role": "user", "content": "What is 1+1?"}]
resp = completion(model="deepseek/deepseek-reasoner", messages=messages, stream=False)

reasoning_content = resp.choices[0].message.provider_specific_fields["reasoning_content"]
content = resp.choices[0].message.content

print(reasoning_content)
print(content)
