# cython: boundscheck=False, wraparound=False, initializedcheck=False
# cython: embedsignature=True

import numpy as np
from libc.stdint cimport int8_t, int32_t

cpdef int32_t[:, :] streak_gen(int8_t[:] streak_start, int min_length):
    cdef int n = streak_start.shape[0]
    cdef int start = 0
    cdef int stop = -1
    cdef int i = 0
    cdef int j, k

    cdef int32_t[:, :] streaks = np.empty((n, 3), dtype=np.int32)

    cdef int8_t* data = &streak_start[0]

    while start < n:
        start = -1
        for k in range(stop + 1, n):
            if data[k] != 0:
                start = k
                break
        if start == -1:
            break

        stop = -1
        for j in range(start, n):
            if data[j] == 0:
                stop = j
                break

        if stop == -1:
            if n - start + 1>= min_length:
                streaks[i, 0] = start
                streaks[i, 1] = n
                streaks[i, 2] = n - start + 1
                i += 1
            break

        elif stop - start + 1 >= min_length:
            streaks[i, 0] = start
            streaks[i, 1] = stop
            streaks[i, 2] = stop - start + 1
            i += 1

    return streaks[:i, :]
