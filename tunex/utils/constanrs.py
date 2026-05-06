"""Default configuration constants for TuneX."""

# Default PID gains
DEFAULT_KP = 2.0
DEFAULT_KI = 0.5
DEFAULT_KD = 0.1

# Default setpoint (target speed)
DEFAULT_SETPOINT = 100.0

# Simulation parameters
SIM_DURATION = 10.0   # seconds
SIM_DT = 0.01         # time step (100 Hz)
SIM_MAX_VOLTAGE = 12.0  # actuator saturation

# Plant model (first-order system: tau * dy/dt + y = K * u)
PLANT_TAU = 0.5   # time constant
PLANT_K = 1.0     # steady-state gain

# UI update delay for animation (ms)
GRAPH_ANIM_INTERVAL = 30
# How many points to append per animation tick
GRAPH_ANIM_CHUNK = 20

# Max history traces to display
MAX_HISTORY_DISPLAY = 5
