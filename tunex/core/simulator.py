"""Simulation engine for a first-order plant with PID controller."""

from typing import Tuple, List
import numpy as np
from tunex.core.pid import PIDController
from tunex.utils.constants import SIM_MAX_VOLTAGE


class FirstOrderPlant:
    """Simple first-order system: tau * dy/dt + y = K * u."""

    def __init__(self, tau: float = 1.0, K: float = 1.0, initial_output: float = 0.0) -> None:
        self.tau = tau
        self.K = K
        self.y = initial_output

    def step(self, u: float, dt: float) -> float:
        """Advance the plant by one time step and return the new output."""
        dy = (-self.y + self.K * u) / self.tau
        self.y += dy * dt
        return self.y

    def reset(self) -> None:
        """Reset plant output to zero."""
        self.y = 0.0


def run_simulation(
    duration: float,
    dt: float,
    setpoint: float,
    kp: float,
    ki: float,
    kd: float,
    tau: float,
    K: float,
) -> Tuple[np.ndarray, np.ndarray, float]:
    """
    Run a closed-loop PID simulation of a first-order plant.

    Returns:
        time: 1D array of time points.
        pv: Process variable (plant output) at each time.
        setpoint: The setpoint value (constant).
    """
    n_steps = int(duration / dt)
    time = np.linspace(0, duration, n_steps)
    pv = np.zeros(n_steps)

    plant = FirstOrderPlant(tau=tau, K=K, initial_output=0.0)
    pid = PIDController(
        kp=kp,
        ki=ki,
        kd=kd,
        setpoint=setpoint,
        output_limits=(-SIM_MAX_VOLTAGE, SIM_MAX_VOLTAGE),
    )
    pid.reset()
    plant.reset()

    for i in range(n_steps):
        # Measure current output
        current_pv = plant.y
        pv[i] = current_pv
        # Compute control action
        u = pid.update(current_pv, dt)
        # Apply to plant
        plant.step(u, dt)

    return time, pv, setpoint
