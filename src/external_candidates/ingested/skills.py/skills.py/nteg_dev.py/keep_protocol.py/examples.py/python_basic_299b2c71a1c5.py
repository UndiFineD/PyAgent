# Extracted from: C:\DEV\PyAgent\.external\skills\skills\nteg-dev\keep-protocol\examples\python_basic.py
#!/usr/bin/env python3
"""Basic example: send a signed packet to a keep server using the SDK."""

from keep.client import KeepClient

client = KeepClient("localhost", 9009)
reply = client.send(
    src="bot:example-agent",
    dst="server",
    body="hello from example",
)
print(f"Server replied: {reply.body}")
