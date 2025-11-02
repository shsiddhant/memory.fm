from __future__ import annotations
from typing import TYPE_CHECKING
import cython
import numpy as np

if TYPE_CHECKING:
    import pandas as pd
    ArrayLike = list | tuple | np.typing.NDArray | pd.Series


@cython.boundscheck(False)
@cython.wraparound(False)
def streak_gen(
    streak_start: cython.bint[:],
    min_length: cython.int,
) -> cython.int[:, :]:
    n: cython.int
    n = streak_start.shape[0]
    start: cython.int = 0
    stop: cython.int = 0
    i: cython.int = 0
    streaks: cython.int[:, :] = np.zeros((n, 3), dtype=np.intc)

    while start < n:
        g = (k for k in range(stop + 1, n) if streak_start[k])
        start = next(g, -1)
        if start == -1:
            break
        h = (j for j in range(start, n) if not streak_start[j])
        stop = next(h, -1)
        if stop == -1:
            if n - start + 1 >= min_length:
                streaks[i, 0] = start
                streaks[i, 1] = n
                streaks[i, 2] =  n - start + 1
            i += 1
            break
        elif stop-start+1 >= min_length:
            streaks[i, 0] = start
            streaks[i, 1] = stop
            streaks[i, 2] = stop - start + 1
            i += 1
    streaks = np.asarray(streaks)[:i, :]
    return streaks
