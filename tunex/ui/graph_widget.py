"""Real-time plot widget based on PyQtGraph."""

from PySide6.QtCore import QTimer, Signal
from PySide6.QtGui import QColor
import pyqtgraph as pg
import numpy as np
from typing import List
from tunex.models.tuning_state import TuningState
from tunex.utils.constants import GRAPH_ANIM_INTERVAL, GRAPH_ANIM_CHUNK, MAX_HISTORY_DISPLAY


class GraphWidget(pg.PlotWidget):
    """
    Custom plot widget that shows setpoint, current simulation and historical traces.
    Supports animated "live" curve drawing.
    """

    animation_finished = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setLabel("left", "Speed", units="rad/s")
        self.setLabel("bottom", "Time", units="s")
        self.showGrid(x=True, y=True, alpha=0.2)
        self.setBackground("#121212")
        self.legend = self.addLegend(offset=(5, 5))

        # Setpoint line (dashed red)
        self.setpoint_curve = self.plot(
            [], [],
            pen=pg.mkPen(color="#ff4c4c", width=2, style=pg.QtCore.Qt.PenStyle.DashLine),
            name="Setpoint"
        )

        # Current simulation trace (bright cyan)
        self.current_curve = self.plot(
            [], [],
            pen=pg.mkPen(color="#00e5ff", width=2.5),
            name="Current"
        )

        # History traces
        self.history_curves: List[pg.PlotDataItem] = []
        self.history_colors = [
            QColor("#ffb74d"), QColor("#81c784"), QColor("#64b5f6"),
            QColor("#ce93d8"), QColor("#fff176")
        ]

        # Animation timer
        self._anim_timer = QTimer()
        self._anim_timer.timeout.connect(self._on_anim_step)
        self._anim_data_time = np.array([])
        self._anim_data_pv = np.array([])
        self._anim_index = 0

    def animate_curve(self, time_arr: np.ndarray, pv_arr: np.ndarray) -> None:
        """Start animating the current response curve."""
        self._anim_data_time = time_arr
        self._anim_data_pv = pv_arr
        self._anim_index = 0
        self.current_curve.setData([], [])
        self._anim_timer.start(GRAPH_ANIM_INTERVAL)

    def _on_anim_step(self) -> None:
        """Append a chunk of points to the current curve."""
        end_idx = min(self._anim_index + GRAPH_ANIM_CHUNK, len(self._anim_data_time))
        if end_idx <= self._anim_index:
            self._anim_timer.stop()
            self.animation_finished.emit()
            return

        x = self._anim_data_time[:end_idx]
        y = self._anim_data_pv[:end_idx]
        self.current_curve.setData(x, y)
        self._anim_index = end_idx

        if end_idx >= len(self._anim_data_time):
            self._anim_timer.stop()
            self.animation_finished.emit()

    def set_setpoint(self, setpoint: float, duration: float) -> None:
        """Display a horizontal setpoint line for the specified duration."""
        self.setpoint_curve.setData([0, duration], [setpoint, setpoint])

    def show_history(self, states: List[TuningState]) -> None:
        """Clear previous history and plot the given states as faded lines."""
        # Remove old history curves
        for curve in self.history_curves:
            self.removeItem(curve)
        self.history_curves.clear()

        # Keep only the most recent MAX_HISTORY_DISPLAY attempts
        recent = states[-MAX_HISTORY_DISPLAY:] if len(states) > MAX_HISTORY_DISPLAY else states

        for i, state in enumerate(recent):
            color = self.history_colors[i % len(self.history_colors)]
            pen = pg.mkPen(color=color, width=1.2, style=pg.QtCore.Qt.PenStyle.SolidLine)
            curve = self.plot(
                state.time_array, state.pv_array,
                pen=pen,
                name=f"Hist #{len(states)-len(recent)+i+1}"
            )
            self.history_curves.append(curve)

    def clear_history(self) -> None:
        """Remove all historical traces."""
        for curve in self.history_curves:
            self.removeItem(curve)
        self.history_curves.clear()
