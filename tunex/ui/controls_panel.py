"""PID tuning controls and simulation start/stop."""

from PySide6.QtWidgets import (
    QWidget, QGroupBox, QFormLayout, QDoubleSpinBox,
    QCheckBox, QPushButton, QVBoxLayout
)
from PySide6.QtCore import Signal
from tunex.utils.constants import DEFAULT_KP, DEFAULT_KI, DEFAULT_KD, DEFAULT_SETPOINT


class ControlsPanel(QWidget):
    """
    Panel with PID gain inputs, setpoint, and action buttons.
    Emits signals for run/reset and history toggle.
    """

    run_simulation_clicked = Signal(float, float, float, float)  # kp, ki, kd, setpoint
    reset_history_clicked = Signal()
    show_history_toggled = Signal(bool)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)

        # PID gains group
        pid_group = QGroupBox("PID Gains")
        form = QFormLayout()
        self.kp_spin = QDoubleSpinBox()
        self.kp_spin.setRange(0.0, 100.0)
        self.kp_spin.setSingleStep(0.1)
        self.kp_spin.setDecimals(3)
        self.kp_spin.setValue(DEFAULT_KP)
        form.addRow("Kp", self.kp_spin)

        self.ki_spin = QDoubleSpinBox()
        self.ki_spin.setRange(0.0, 10.0)
        self.ki_spin.setSingleStep(0.01)
        self.ki_spin.setDecimals(4)
        self.ki_spin.setValue(DEFAULT_KI)
        form.addRow("Ki", self.ki_spin)

        self.kd_spin = QDoubleSpinBox()
        self.kd_spin.setRange(0.0, 5.0)
        self.kd_spin.setSingleStep(0.01)
        self.kd_spin.setDecimals(4)
        self.kd_spin.setValue(DEFAULT_KD)
        form.addRow("Kd", self.kd_spin)

        pid_group.setLayout(form)
        layout.addWidget(pid_group)

        # Setpoint
        sp_group = QGroupBox("Setpoint")
        sp_form = QFormLayout()
        self.setpoint_spin = QDoubleSpinBox()
        self.setpoint_spin.setRange(0.0, 200.0)
        self.setpoint_spin.setSingleStep(1.0)
        self.setpoint_spin.setDecimals(1)
        self.setpoint_spin.setValue(DEFAULT_SETPOINT)
        sp_form.addRow("Target (rad/s)", self.setpoint_spin)
        sp_group.setLayout(sp_form)
        layout.addWidget(sp_group)

        # Options & actions
        self.show_history_check = QCheckBox("Show Previous Attempts")
        self.show_history_check.stateChanged.connect(
            lambda state: self.show_history_toggled.emit(state == 2)
        )
        layout.addWidget(self.show_history_check)

        self.run_btn = QPushButton("Run Simulation")
        self.run_btn.clicked.connect(self._on_run)
        layout.addWidget(self.run_btn)

        self.reset_btn = QPushButton("Reset History")
        self.reset_btn.clicked.connect(self.reset_history_clicked.emit)
        layout.addWidget(self.reset_btn)

        layout.addStretch()

    def _on_run(self) -> None:
        """Emit run signal with current values."""
        self.run_simulation_clicked.emit(
            self.kp_spin.value(),
            self.ki_spin.value(),
            self.kd_spin.value(),
            self.setpoint_spin.value()
        )
