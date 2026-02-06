# Extracted from: C:\DEV\PyAgent\.external\agentcloud\agent-backend\src\main.py
import logging
import signal
import threading
import time
from asyncio import CancelledError
from contextlib import asynccontextmanager

from fastapi import FastAPI
from init.env_variables import LOG_LEVEL, MAX_THREADS
from langchain.globals import set_debug, set_verbose
from messaging.client import consume_tasks

app_logger = logging.getLogger("app")

app_logger.setLevel(LOG_LEVEL.upper())

# disable this once LOG_LEVEL is properly imported from .env
set_debug(True)
set_verbose(True)


def sigint_handler(*args):
    raise SystemExit("Got SIGINT. Exiting...")


@asynccontextmanager
async def lifespan(app: FastAPI):
    signal.signal(signal.SIGINT, sigint_handler)

    print("running lifespan function")

    try:
        if threading.active_count() < MAX_THREADS:
            await consume_tasks()
        else:
            print("All threads are busy...will try again")
            time.sleep(10)
            await consume_tasks()
        yield
    except CancelledError:
        pass


app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    print("hello world")
