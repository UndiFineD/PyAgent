# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\core\scheduler\simple_queue_mixin.py
import os
import time
import traceback
from abc import ABC
from multiprocessing.managers import BaseManager
from queue import Queue
from typing import Any


class SimpleQueueMixin(ABC):
    """Class that adds a simple queue-based worker scheduler to a submission system."""

    def has_queue(self):
        return "queue" in self.submission_args

    def _queue_get_address(self):
        host_port = self.submission_args.get("queue", None)
        if not host_port:
            raise ValueError(
                f"No host:port specified for this scheduler, 'queue' field missing in submission_args of scheduler {self.name}"
            )
        if ":" not in host_port:
            raise ValueError(
                f"Invalid host:port {host_port} specified for scheduler {self.name}"
            )
        host, port_str = host_port.split(":", 1)
        try:
            port = int(port_str)
        except ValueError:
            raise ValueError(
                f"Invalid port {port_str} specified for scheduler {self.name}"
            )
        return host, port

    def queue_put(self, job_id: str, task: Any):
        """Put a task into the queue to be processed by a worker."""
        queue = self.connect_to_queue()
        queue.put((job_id, task))

    def queue_size(self, job_id: str = None) -> int | None:
        """Get number of tasks in the queue (not running yet)
           or None if queue is not used or job_id is already running (or not found).

        :param job_id: If specified, get the position of the job
                       in the queue: None = running (probably), 0 = next to run, 1 = one job ahead, etc.
        :return: Number of tasks or None
        """
        if not self.has_queue():
            return None
        queue = self.connect_to_queue()
        if job_id is not None:
            job_ids = queue.get_job_ids()
            return job_ids.index(job_id) if job_id in job_ids else None
        else:
            return queue.qsize()

    def connect_to_queue(self, host: str = None, port: int = None):
        """Connects to the queue server and returns the queue object."""
        BaseManager.register("get_queue")
        default_host, default_port = self._queue_get_address()
        host = host or default_host
        port = port or default_port
        manager = BaseManager(address=(host, port), authkey=self._queue_get_auth_key())
        try:
            manager.connect()
            return manager.get_queue()
        except ConnectionRefusedError:
            raise ConnectionError(
                f"Could not connect to queue server at {':'.join(map(str, self._queue_get_address()))}. Is the ovo scheduler worker running?"
            )

    def create_queue_server(self, host: str = None, port: int = None):
        """Returns queue and function that runs infinitely in the server process, serving the queue to workers."""
        queue = TaskQueue()
        BaseManager.register("get_queue", callable=lambda: queue)
        default_host, default_port = self._queue_get_address()
        host = host or default_host
        port = port or default_port
        manager = BaseManager(address=(host, port), authkey=self._queue_get_auth_key())
        server = manager.get_server()
        print(f"Queue server starting on {host}:{port}")
        return queue, server.serve_forever

    def queue_worker(self, queue, queue_id):
        """Function that runs infinitely in the worker process, processing jobs from the queue."""
        print(f"Worker {queue_id} connected to queue")
        while True:
            item = queue.get()
            if item is None:
                # Shutdown signal
                print(f"Worker {queue_id} shutting down")
                return
            if not isinstance(item, tuple) or len(item) != 2:
                print(f"Worker {queue_id} received invalid task: {item} ({type(item)})")
                continue
            job_id, task = item
            print(f"Worker {queue_id} executing task: {task}")
            try:
                start_time = time.time()
                self.queue_run_task(job_id, task)
                seconds = time.time() - start_time
                print(
                    f"Worker {queue_id} finished command in {int(seconds) // 60} minutes {seconds % 60:.0f} seconds"
                )
            except Exception as e:
                traceback.print_exc()
                print(f"Worker {queue_id} encountered error: {e}")

    def queue_run_task(self, job_id: str, task: Any):
        """Execute a single task from the queue synchronously - executed in the worker loop"""
        raise NotImplementedError()

    def _queue_get_auth_key(self):
        return os.environ.get("OVO_WORKER_AUTHKEY", "no_key").encode("utf-8")


class TaskQueue:
    def __init__(self):
        self.q = Queue()

    def put(self, item):
        return self.q.put(item)

    def get(self):
        return self.q.get()

    def get_job_ids(self):
        with self.q.mutex:
            return [item[0] for item in self.q.queue]
