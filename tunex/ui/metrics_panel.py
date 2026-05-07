"""Panel displaying performance metrics of the latest simulation."""
import numpy as np
from PySide6.QtWidgets import QWidget, QGroupBox, QFormLayout, QLabel
from PySide6.QtCore import Qt


class MetricsPanel(QWidget):
    """Shows overshoot, settling time, steady-state error, rise time."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        layout = QFormLayout(self)
        self.setLayout(layout)

        group = QGroupBox("Performance Metrics")
        form = QFormLayout()

        self.overshoot_label = QLabel("-- %")
        form.addRow("Overshoot:", self.overshoot_label)

        self.settling_label = QLabel("-- s")
        form.addRow("Settling Time (2%):", self.settling_label)

        self.steady_err_label = QLabel("--")
        form.addRow("Steady-State Error:", self.steady_err_label)

        self.rise_label = QLabel("-- s")
        form.addRow("Rise Time (10%-90%):", self.rise_label)

        group.setLayout(form)
        layout.addWidget(group)

    def update_metrics(
        self,
        overshoot: float,
        settling_time: float,
        steady_state_error: float,
        rise_time: float,
    ) -> None:
        """Format and display new metric values."""
        self.overshoot_label.setText(f"{overshoot:.2f} %")
        self.settling_label.setText(f"{settling_time:.4f} s")
        self.steady_err_label.setText(f"{steady_state_error:.4f} rad/s")
        if np.isnan(rise_time):
            self.rise_label.setText("N/A")
        else:
            self.rise_label.setText(f"{rise_time:.4f} s")
