from swarm.task_scheduler import TaskScheduler


def test_enqueue_dequeue_priority():
    """Tasks should be dequeued in order of priority (lower number = higher priority)."""
    sched = TaskScheduler()
    t1 = sched.enqueue({"name": "a"}, priority=2)
    t2 = sched.enqueue({"name": "b"}, priority=1)
    first = sched.dequeue()
    assert first["payload"]["name"] == "b"
    second = sched.dequeue()
    assert second["payload"]["name"] == "a"


def test_modify_priority():
    """Modifying a task's priority should update its stored priority, even if it doesn't requeue the task."""
    sched = TaskScheduler()
    t = sched.enqueue({"x":1}, priority=3)
    sched.modify(t, priority=1)
    # even though modify doesn't requeue, the stored priority should reflect change
    assert sched._tasks[t]["priority"] == 1
