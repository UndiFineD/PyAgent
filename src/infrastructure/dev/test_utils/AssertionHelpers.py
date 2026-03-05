"""Minimal AssertionHelpers shim for dev test utilities."""


class AssertionHelpers:
    @staticmethod
    def expect_exception(exc_type, callable_obj, *args, **kwargs):
        try:
            callable_obj(*args, **kwargs)
        except Exception as e:
            return isinstance(e, exc_type)
        return False
