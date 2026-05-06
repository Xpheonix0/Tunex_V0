"""Iterative tuner: manages history of tuning attempts and emits signals."""

from PySide6.QtCore import QObject, Signal
from tunex.models.tuning_state import TuningState
from typing import List
import datetime


class IterativeTuner(QObject):
    """
    Holds the history of PID tuning attempts.
    Emits simulation_completed after each new attempt.
    """

    simulation_completed = Signal(TuningState)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.history: List[TuningState] = []
        self.current_state: TuningState | None = None

    def add_attempt(
        self,
        kp: float,
        ki: float,
        kd: float,
        time_array,
        pv_array,
        setpoint: float,
        overshoot: float,
        settling_time: float,
        steady_state_error: float,
        rise_time: float,
    ) -> None:
        """Store a new tuning attempt and emit signal."""
        state = TuningState(
            kp=kp,
            ki=ki,
            kd=kd,
            time_array=time_array.copy(),
            pv_array=pv_array.copy(),
            setpoint=setpoint,
            overshoot=overshoot,
            settling_time=settling_time,
            steady_state_error=steady_state_error,
            rise_time=rise_time,
            timestamp=datetime.datetime.now(),
        )
        self.current_state = state
        self.history.append(state)
        self.simulation_completed.emit(state)

    def clear_history(self) -> None:
        """Remove all previous tuning attempts (keep current state if any)."""
        self.history.clear()
        self.current_state = None
