# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pdf-extract-api\app\celery_config.py
import multiprocessing

from celery import Celery

multiprocessing.set_start_method("spawn", force=True)


def make_celery():
    celery = Celery("app", broker="redis://redis:6379/0", backend="redis://redis:6379/0")
    celery.config_from_object({"worker_max_memory_per_child": 8200000})
    return celery


celery = make_celery()
