import time
from typing import Callable, TypeVar

T = TypeVar("T")


def measure_latency_ms(function: Callable[[], T]) -> tuple[T, int]:
    start_time = time.perf_counter()

    result = function()

    end_time = time.perf_counter()

    latency_ms = int((end_time - start_time) * 1000)

    return result, latency_ms