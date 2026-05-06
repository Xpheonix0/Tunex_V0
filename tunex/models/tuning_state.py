"""Data class holding a single tuning attempt and its results."""

from dataclasses import dataclass, field
from typing import List
import numpy as np
import datetime


@dataclass
class TuningState:
    kp: float
    ki: float
    kd: float
    time_array: np.ndarray
    pv_array: np.ndarray
    setpoint: float
    overshoot: float
    settling_time: float
    steady_state_error: float
    rise_time: float
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)
