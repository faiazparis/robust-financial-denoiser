from __future__ import annotations
from rpsd.features import sliding_windows

def test_bounds_cover_all_cases():
    # n < window -> single window
    assert sliding_windows(10, 100, 0.5) == [(0, 10)]
    # standard case
    b = sliding_windows(1000, 200, 0.5)
    assert b[0] == (0, 200)
    assert b[-1] == (800, 1000)
    # overlap edge and rounding
    b2 = sliding_windows(101, 20, 0.33)
    assert b2[0] == (0, 20) and b2[-1] == (91, 101)
