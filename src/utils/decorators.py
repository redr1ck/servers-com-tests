"""Utility decorators for test helpers."""
from functools import wraps
from typing import Callable, Any, Optional
from playwright.sync_api import Page


def retry_on_condition(
    page: Page,
    max_retries: int = 3,
    wait_ms: int = 1000,
    condition_func: Callable[[Any], bool] = None,
):
    """
    Retry decorator that retries if condition_func returns True.

    Args:
        page: Playwright Page object for wait_for_timeout
        max_retries: Maximum number of retries
        wait_ms: Wait time between retries in milliseconds
        condition_func: Function that returns True if retry is needed
                       Receives the return value of decorated function

    Example:
        @retry_on_condition(page, max_retries=3, wait_ms=1000, condition_func=lambda row: row is not None)
        def _check_contact_deleted() -> Optional[ContactTableRow]:
            return self.get_row_by_contact_id(contact_id)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_error = None

            for attempt in range(max_retries):
                try:
                    result = func(*args, **kwargs)

                    # If condition_func is provided, check it
                    if condition_func:
                        if condition_func(result):
                            # Condition is True - need to retry
                            if attempt < max_retries - 1:
                                page.wait_for_timeout(wait_ms)
                                continue
                            else:
                                # Max retries reached, return result
                                return result

                    # Success or condition is False
                    return result

                except Exception as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        page.wait_for_timeout(wait_ms)
                        continue
                    else:
                        raise

            # If we get here, retries exhausted
            if last_error:
                raise last_error
            return None

        return wrapper
    return decorator

