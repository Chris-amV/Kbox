import logging
import math
from typing import Any

import numpy as np
import plotly.graph_objects as go
import staliro

from staliro.core import best_eval, best_run
from staliro.models import State, ode
from staliro.optimizers import UniformRandom
from staliro.options import Options
from staliro.specifications import RTAMTDense
from staliro.staliro import simulate_model, staliro
from box import point

from typing import Callable, Generic, Iterable, Iterator, Sequence, Tuple, TypeVar, Union
import time

# THIS FILE CONTAINS THE REAL FORMULAS AND THE ORECAL FUNCTION

T = TypeVar("T")
def _time(func: Callable[[], T]) -> Tuple[float, T]:
    start_time = time.perf_counter()
    result = func()
    stop_time = time.perf_counter()
    duration = stop_time - start_time

    return duration, result

# THE FORMULAS

phi = r"(always[1,2] (eventually[3,4] (x1 >= 3 and x1 <= 10)) -> (x1 >= 0 and x1 <= 10)) and (always (x1 >= -20 and x1 <= 20))"
# phi = r"always !(a >= -1.6 and a <= -1.4  and b >= -1.1 and b <= -0.9)"
phi1 = r"(always[1,2] (eventually[3,4] (x1 >= 3 and x1 <= 10)) -> (x1 >= 0 and x1 <= 10)) and (always (x1 >= -20 and x1 <= 20))"
phi2 = r"(always[0,1] (eventually[7,8] (x1 >= 3 and x1 <= 10)) -> (always[0,1] (eventually[14,15] (x1 >= 0 and x1 <= 10)))) and (always (x1 >= -20 and x1 <= 20))"
phi100= r"(always[0,1] (eventually[30,31] (x1 >= 3 and x1 <= 10)) -> (always[0,1] (eventually[60,70] (x1 >= 0 and x1 <= 10)))) and (always (x1 >= -20 and x1 <= 20))"
phi50 = r"(always (x1 >= -20 and x1 <= 3) -> (eventually (x1 >= 3 and x1 <= 45))) and (always (x1 >= -50 and x1 <= 50))"   

phi = r"(always[0,15] (x1 >=0 and x1<=2350)) and (always (x1 >= -2350 and x1 <= 2350))"
specification = RTAMTDense(phi50, {"x1":0})

# THE ORECAL FUNCTION
def d2(p):
    point_coord = [p.coord]
    point_time = []
    for i in range(0,p.dim):
        point_time.append(i)
    compute_cost = lambda: specification.evaluate(point_coord, point_time)
    cost_duration, cost = _time(compute_cost)
    return cost

if __name__ == "__main__":
    pass
