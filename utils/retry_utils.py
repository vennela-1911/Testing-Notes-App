import time
import functools

from typing import Callable, Type, Tuple, Any, Optional

from http.client import RemoteDisconnected

from urllib3.exceptions import (
    MaxRetryError,
    ProtocolError,
)

from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementNotInteractableException,
    ElementClickInterceptedException,
    TimeoutException,
)

from config.environment import config
from utils.logger import get_logger


logger = get_logger(__name__)


# Retry only genuine Selenium flaky UI exceptions
DEFAULT_SELENIUM_EXCEPTIONS: Tuple[Type[Exception], ...] = (
    StaleElementReferenceException,
    ElementNotInteractableException,
    ElementClickInterceptedException,
    TimeoutException,
)


# Infrastructure/Grid fatal errors
FATAL_GRID_ERRORS: Tuple[Type[Exception], ...] = (
    MaxRetryError,
    ProtocolError,
    RemoteDisconnected,
    ConnectionRefusedError,
)


def retry(
    max_attempts: int = config.timeouts.retry_attempts,
    delay: float = config.timeouts.retry_delay,
    exceptions: Tuple[Type[Exception], ...] = DEFAULT_SELENIUM_EXCEPTIONS,
    on_retry: Optional[Callable] = None,
):
    """
    Decorator that retries flaky Selenium actions.

    Retries only UI interaction instability.
    Fails fast on Selenium Grid / infrastructure failures.

    Example:

        @retry(max_attempts=3, delay=1)
        def click_button():
            driver.find_element(...).click()
    """

    def decorator(func: Callable) -> Callable:

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:

            last_exc = None

            for attempt in range(1, max_attempts + 1):

                try:

                    result = func(*args, **kwargs)

                    if attempt > 1:
                        logger.info(
                            f"[RETRY] '{func.__name__}' "
                            f"succeeded on attempt {attempt}"
                        )

                    return result

                except Exception as exc:

                    # Fail immediately for Selenium Grid crashes
                    if isinstance(exc, FATAL_GRID_ERRORS):

                        logger.error(
                            f"[FATAL GRID ERROR] "
                            f"{type(exc).__name__}: {exc}"
                        )

                        raise

                    # Retry only allowed Selenium flaky exceptions
                    if isinstance(exc, exceptions):

                        last_exc = exc

                        logger.warning(
                            f"[RETRY] '{func.__name__}' "
                            f"attempt {attempt}/{max_attempts} failed: "
                            f"{type(exc).__name__}: {exc}"
                        )

                        if on_retry:
                            on_retry(attempt, exc)

                        if attempt < max_attempts:
                            time.sleep(delay)

                        continue

                    # Unknown exception → fail immediately
                    raise

            logger.error(
                f"[RETRY] '{func.__name__}' "
                f"failed after {max_attempts} attempts"
            )

            raise last_exc

        return wrapper

    return decorator


def retry_action(
    action: Callable,
    max_attempts: int = config.timeouts.retry_attempts,
    delay: float = config.timeouts.retry_delay,
    exceptions: Tuple[Type[Exception], ...] = DEFAULT_SELENIUM_EXCEPTIONS,
) -> Any:
    """
    Inline retry helper for one-off Selenium actions.

    Example:

        retry_action(
            lambda: driver.find_element(...).click()
        )
    """

    last_exc = None

    for attempt in range(1, max_attempts + 1):

        try:

            return action()

        except Exception as exc:

            # Fail immediately for infrastructure/Grid failures
            if isinstance(exc, FATAL_GRID_ERRORS):

                logger.error(
                    f"[FATAL GRID ERROR] "
                    f"{type(exc).__name__}: {exc}"
                )

                raise

            if isinstance(exc, exceptions):

                last_exc = exc

                logger.warning(
                    f"[RETRY ACTION] "
                    f"attempt {attempt}/{max_attempts} failed: "
                    f"{type(exc).__name__}: {exc}"
                )

                if attempt < max_attempts:
                    time.sleep(delay)

                continue

            raise

    logger.error(
        f"[RETRY ACTION] "
        f"failed after {max_attempts} attempts"
    )

    raise last_exc


def wait_and_retry(
    condition: Callable[[], bool],
    max_attempts: int = 5,
    delay: float = 0.5,
    label: str = "condition",
) -> bool:
    """
    Polls until condition() returns True.

    Useful for:
    - DOM updates
    - delayed rendering
    - async UI validations
    """

    for attempt in range(1, max_attempts + 1):

        try:

            if condition():

                logger.debug(
                    f"[WAIT-RETRY] '{label}' "
                    f"met on attempt {attempt}"
                )

                return True

        except Exception as exc:

            # Infrastructure failure → stop immediately
            if isinstance(exc, FATAL_GRID_ERRORS):

                logger.error(
                    f"[FATAL GRID ERROR] "
                    f"{type(exc).__name__}: {exc}"
                )

                raise

            logger.debug(
                f"[WAIT-RETRY] '{label}' "
                f"attempt {attempt} raised: {exc}"
            )

        if attempt < max_attempts:
            time.sleep(delay)

    logger.warning(
        f"[WAIT-RETRY] '{label}' "
        f"not met after {max_attempts} attempts"
    )

    return False