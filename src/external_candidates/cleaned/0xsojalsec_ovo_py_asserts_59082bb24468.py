# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_ovo.py\tests.py\unit_tests.py\utils.py\asserts_59082bb24468.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\tests\unit_tests\utils\asserts.py

from typing import Any

from streamlit.testing.v1 import AppTest


def assert_equal(expected: Any, actual: Any, step: str) -> None:
    """Assert that two parameters are equal.

    Args:

        expected (Any): expected value

        actual (Any): actual value

        step (str): description of the step, which is tested

    """

    assert expected == actual, f"{step}\nexpected: {expected}\nActual: {actual}\n--------------------\n"


def assert_not_equal(expected: Any, actual: Any, step: str) -> None:
    """Assert that two parameters are NOT equal.

    Args:

        expected (Any): expected value

        actual (Any): actual value

        step (str): description of the step, which is tested

    """

    assert expected != actual, f"{step}\nexpected: {expected}\nActual: {actual}\n--------------------\n"


def assert_true(value: Any, step: str) -> None:
    """Assert that value is true

    Args:

        value (Any): value to check

        step (str): description of the step, which is tested

    """

    assert value, f"{step}\nvalue: {value}\n--------------------\n"


def assert_false(value: Any, step: str) -> None:
    """Assert that value is false

    Args:

        value (Any): value to check

        step (str): description of the step, which is tested

    """

    assert not value, f"{step}\nvalue: {value}\n--------------------\n"


def assert_element_exists(widget_list: Any, key: str, step: str) -> None:
    """Assert, that element with given key exists on page.

    Args:

        widget_list (WidgetList): sequence of elements (e.g. at.button)

        key (str): key of the elements

        step (str): description of the step, which is tested

    """

    try:
        widget_list(key)

        assert True

    except KeyError:
        assert False, f"{step}\nkey: {key}\n--------------------\n"


def assert_no_error_on_page(at: AppTest, page_name: str) -> None:
    """Assert, that there is no error on given page.

    Args:

        at (AppTest): app test instance

        page_name (str): name of page to be logged

    """

    assert not at.error, (
        f"Verify, that, there is no error on page {page_name}\n"
        f"value: {[error.value for error in at.error]}\n"
        "--------------------\n"
    )


def assert_no_error_on_exception(at: AppTest, exception_text: str) -> None:
    """Assert, that there is no error on page durin handling an exception.

    Args:

        at (AppTest): app test instance

        exception_text (str): text of an error to be logged

    """

    assert not at.error, (
        f"Exception catched: {exception_text}\n"
        f"error on page: {[error.value for error in at.error]}\n"
        "--------------------\n"
    )
