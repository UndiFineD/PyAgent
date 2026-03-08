"""Minimal placeholder for torch._C._distributed_c10d containing ProcessGroup."""

class ProcessGroup:
    """Lightweight placeholder for distributed ProcessGroup used during import.

    Real distributed functionality is not implemented; this exists only to
    satisfy import-time references during test collection.
    """

    def __init__(self, *args, **kwargs):
        pass
