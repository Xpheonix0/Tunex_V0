"""Main application window that orchestrates everything."""

from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QStatusBar
from PySide6.QtCore import Qt

from tunex.ui.graph_widget import GraphWidget
from tunex.ui.controls_panel import ControlsPanel
from tunex.ui.metrics_panel import MetricsPanel
from tunex.core.simulator import run_simulation
from tunex.core.metrics import compute_metrics
from tunex.core.tuner import IterativeTuner
from tunex.utils.constants import (
    SIM_DURATION, SIM_DT, DEFAULT_SETPOINT,
    PLANT_TAU, PLANT_K
)
import numpy as np


class MainWindow(QMainWindow):
    """Central application window."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("TuneX – PID Tuning Studio")
        self.resize(1200, 750)

        # Core
        self.tuner = IterativeTuner()
        self.tuner.simulation_completed.connect(self._on_simulation_completed)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        # Left: Graph
        self.graph = GraphWidget()
        main_layout.addWidget(self.graph, stretch=3)

        # Right: controls + metrics
        right_panel = QVBoxLayout()
        self.controls = ControlsPanel()
        self.metrics = MetricsPanel()
        right_panel.addWidget(self.controls)
        right_panel.addWidget(self.metrics)
        right_panel.addStretch()

        right_widget = QWidget()
        right_widget.setLayout(right_panel)
        right_widget.setMaximumWidth(320)
        main_layout.addWidget(right_widget)

        # Connections
        self.controls.run_simulation_clicked.connect(self._start_simulation)
        self.controls.reset_history_clicked.connect(self._reset_history)
        self.controls.show_history_toggled.connect(self._toggle_history)
        self.graph.animation_finished.connect(self._animation_done)

        # Status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Ready")

        # Initial empty setpoint line
        self.graph.set_setpoint(DEFAULT_SETPOINT, SIM_DURATION)

    def _start_simulation(self, kp: float, ki: float, kd: float, setpoint: float) -> None:
        """Run simulation, display live animation, compute metrics."""
        self.status.showMessage("Simulation running…")
        # Disable run button to prevent double clicks
        self.controls.run_btn.setEnabled(False)

        # Run simulation (fast, in main thread)
        time_arr, pv_arr, sp = run_simulation(
            duration=SIM_DURATION,
            dt=SIM_DT,
            setpoint=setpoint,
            kp=kp,
            ki=ki,
            kd=kd,
            tau=PLANT_TAU,
            K=PLANT_K,
        )

        # Compute metrics immediately
        overshoot, settle, sse, rise = compute_metrics(time_arr, pv_arr, setpoint)

        # Store attempt in tuner (will emit signal)
        self.tuner.add_attempt(kp, ki, kd, time_arr, pv_arr, setpoint,
                               overshoot, settle, sse, rise)

        # Update graph: setpoint line and animate
        self.graph.set_setpoint(setpoint, SIM_DURATION)

        # Show/hide history based on checkbox
        self._update_history_visibility()

        # Start live animation of the new trace
        self.graph.animate_curve(time_arr, pv_arr)

    def _on_simulation_completed(self, state) -> None:
        """Slot called when a new tuning state is added."""
        # Update metrics panel
        self.metrics.update_metrics(
            state.overshoot,
            state.settling_time,
            state.steady_state_error,
            state.rise_time,
        )

    def _animation_done(self) -> None:
        """Re-enable UI after animation finishes."""
        self.controls.run_btn.setEnabled(True)
        self.status.showMessage("Simulation complete")

    def _reset_history(self) -> None:
        """Clear all tuning history."""
        self.tuner.clear_history()
        self.graph.clear_history()
        self.metrics.update_metrics(0, 0, 0, 0)  # reset display

    def _toggle_history(self, visible: bool) -> None:
        """Show or hide historical traces."""
        self._update_history_visibility()

    def _update_history_visibility(self) -> None:
        """Refresh the history curves on the graph."""
        if self.controls.show_history_check.isChecked():
            self.graph.show_history(self.tuner.history[:-1])  # exclude current
        else:
            self.graph.clear_history()
