"""Standard PID controller with integral anti-windup."""

from typing import Tuple, Optional


class PIDController:
    """Discrete PID controller with output clamping and integral windup prevention."""

    def __init__(
        self,
        kp: float = 1.0,
        ki: float = 0.0,
        kd: float = 0.0,
        setpoint: float = 0.0,
        output_limits: Tuple[float, float] = (-float("inf"), float("inf")),
    ) -> None:
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.output_limits = output_limits

        self._integral = 0.0
        self._prev_error = 0.0
        # Pre-compute integral clamping bounds (if ki != 0)
        self._integral_min = output_limits[0] if ki != 0 else 0.0
        self._integral_max = output_limits[1] if ki != 0 else 0.0

    def update(self, pv: float, dt: float) -> float:
        """
        Compute the control output for the given process variable and time step.

        Args:
            pv: Process variable (measured value).
            dt: Time since last update (seconds).

        Returns:
            Control signal (clamped to output_limits).
        """
        error = self.setpoint - pv

        # Proportional
        p_out = self.kp * error

        # Integral with clamping (anti-windup)
        self._integral += error * dt
        if self.ki != 0.0:
            self._integral = max(self._integral_min, min(self._integral_max, self._integral))
        i_out = self.ki * self._integral

        # Derivative (on error)
        derivative = (error - self._prev_error) / dt if dt > 0 else 0.0
        d_out = self.kd * derivative
        self._prev_error = error

        output = p_out + i_out + d_out
        # Clamp final output
        output = max(self.output_limits[0], min(self.output_limits[1], output))
        return output

    def reset(self) -> None:
        """Reset controller state (integral and previous error)."""
        self._integral = 0.0
        self._prev_error = 0.0

    def set_gains(self, kp: float, ki: float, kd: float) -> None:
        """Update PID gains and recompute integral limits."""
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self._integral_min = self.output_limits[0] if ki != 0 else 0.0
        self._integral_max = self.output_limits[1] if ki != 0 else 0.0
        # Reset integral to avoid sudden jump after gain change
        self._integral = max(self._integral_min, min(self._integral_max, self._integral))
