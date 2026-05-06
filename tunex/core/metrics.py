"""Performance metric calculations for step responses."""

from typing import Tuple
import numpy as np


def _find_settling_index(
    time: np.ndarray, pv: np.ndarray, final_value: float, tolerance: float = 0.02
) -> int:
    """
    Return the first index after which the signal stays within
    tolerance * |final_value| of the final value.
    """
    if final_value == 0:
        band = 1e-6
    else:
        band = tolerance * abs(final_value)
    # Work backwards to find the last time the signal leaves the band
    within = np.abs(pv - final_value) <= band
    if not np.any(within):
        return len(pv) - 1
    last_out_idx = np.where(~within)[0]
    if len(last_out_idx) == 0:
        return 0
    return last_out_idx[-1] + 1


def compute_metrics(
    time: np.ndarray, pv: np.ndarray, setpoint: float
) -> Tuple[float, float, float, float]:
    """
    Calculate step-response metrics.

    Returns:
        overshoot_pct: Overshoot as % of final value.
        settling_time: Time to settle within 2% of final value.
        steady_state_error: Final value - setpoint.
        rise_time: Time to go from 10% to 90% of final value.
    """
    final_val = pv[-1]
    steady_state_error = setpoint - final_val

    # Overshoot (positive overshoot only)
    if final_val != 0:
        max_val = np.max(pv)
        overshoot_pct = 100.0 * (max_val - final_val) / abs(final_val) if max_val > final_val else 0.0
    else:
        overshoot_pct = 0.0

    # Settling time (2% of final value)
    settle_idx = _find_settling_index(time, pv, final_val, tolerance=0.02)
    settling_time = time[settle_idx] if settle_idx < len(time) else time[-1]

    # Rise time (10% to 90%)
    if final_val != 0:
        t10_val = 0.1 * final_val
        t90_val = 0.9 * final_val
        # find indices crossing these thresholds
        idx10 = np.where(pv >= t10_val)[0]
        idx90 = np.where(pv >= t90_val)[0]
        if len(idx10) > 0 and len(idx90) > 0:
            t_rise = time[idx90[0]] - time[idx10[0]]
        else:
            t_rise = float("nan")
    else:
        t_rise = 0.0

    return overshoot_pct, settling_time, steady_state_error, t_rise
