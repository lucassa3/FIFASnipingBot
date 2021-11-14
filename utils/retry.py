from typing import Tuple
from state.program_state import State
import time as t


def retry(func, wait_time: int, limit: int, *args) -> Tuple[object, str, bool]:
    """Retries function call until not an exception or limit of time exceeded

    Parameters:
    func (object): callable to execute
    wait_time (int): time to wait (sleep -- in seconds) between retries
    limit (int): limit of time (in seconds) to retry call

    Returns:
    object: Returning value of the callable
    str: func name
    bool: succeeds or not
    """

    begin = t.time()

    print(func.__name__)

    while True:
        if State.stop_thread_flag:
            raise ValueError("Waiting for thread to be killed")

        if limit > 0:
            cur = t.time()
            if cur - begin > limit:
                return None, func.__name__, False

        ret, fname, ok = try_func(func, *args)
        if ok:
            return ret, fname, True

        t.sleep(wait_time)


def retry_many(
    funcs, wait_time: int, limit: int, args_list
) -> Tuple[object, str, bool]:
    """Retries array of function calls until not an exception or limit of time exceeded

    Parameters:
    funcs (object): array of func callables to execute
    wait_time (int): time to wait (sleep -- in seconds) between retries
    limit (int): limit of time (in seconds) to retry call

    Returns:
    object: Returning value of the last attempted func call
    str: func name
    bool: succeeds or not
    """
    begin = t.time()

    print(f.__name__ for f in funcs)

    while True:
        for func, args in zip(funcs, args_list):
            if State.stop_thread_flag:
                raise ValueError("Waiting for thread to be joined")

            if limit > 0:
                cur = t.time()
                if cur - begin > limit:
                    return None, func.__name__, False

            ret, fname, ok = try_func(func, *args)
            if ok:
                return ret, fname, True

        t.sleep(wait_time)


def try_func(func, *args) -> Tuple[object, str, bool]:
    try:
        ret = func(*args)
    except Exception as e:
        return None, func.__name__, False
    else:
        return ret, func.__name__, True
