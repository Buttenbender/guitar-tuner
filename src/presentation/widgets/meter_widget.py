# Meter widget - visual tuning meter with needle indicator
# Displays a semicircular gauge showing if the note is sharp, flat or in tune

import tkinter as tk
import customtkinter as ctk
import math

from src.infrastructure.config.constants import COLORS


class MeterWidget(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=COLORS["surface"],
            **kwargs
        )

        # Meter dimensions
        self.width = 420
        self.height = 240

        self.center_x = self.width // 2
        self.center_y = self.height - 35

        self.radius = 125

        self.canvas = tk.Canvas(
            self,
            width=self.width,
            height=self.height,
            bg=COLORS["surface"],
            highlightthickness=0
        )
        self.canvas.pack(padx=20, pady=20)

        self._current_angle = 0.0
        self._target_angle = 0.0
        self._animation_running = False

        self._draw_meter_background()

        self._needle = None
        self._draw_needle()

    def _angle_to_rad(self, angle):
        # Convers:
        #   -90° = left
        #   0° = up
        #   +90° = right
        return math.radians(angle - 90)

    def _point_on_arc(self, angle, radius):
        rad = self._angle_to_rad(angle)

        x = self.center_x + radius * math.cos(rad)
        y = self.center_y + radius * math.sin(rad)

        return x, y

    def _draw_meter_background(self):
        arc_width = 18

        # Left red zone (very flat)
        self._draw_arc_segment(
            -90,
            -15,
            COLORS["very_off"],
            arc_width
        )

        # Left yellow zone (slightly flat)
        self._draw_arc_segment(
            -15,
            -5,
            COLORS["slightly_off"],
            arc_width
        )

        # Center green zone (in tune)
        self._draw_arc_segment(
            -5,
            5,
            COLORS["perfect"],
            arc_width
        )

        # Right yellow zone (slightly sharp)
        self._draw_arc_segment(
            5,
            15,
            COLORS["slightly_off"],
            arc_width
        )

        # Right red zone (very sharp)
        self._draw_arc_segment(
            15,
            90,
            COLORS["very_off"],
            arc_width
        )

        # Main tick marks
        for angle in [-90, -45, -15, 0, 15, 45, 90]:
            self._draw_tick_mark(angle)

        # Cents labels
        labels = [
            (-50, -90),
            (-25, -45),
            (0, 0),
            (25, 45),
            (50, 90),
        ]

        for value, angle in labels:
            x, y = self._point_on_arc(
                angle,
                self.radius + 28
            )

            self.canvas.create_text(
                x,
                y,
                text=f"{value:+d}" if value != 0 else "0",
                fill=COLORS["text_secondary"],
                font=("Segoe UI", 10)
            )

    def _draw_arc_segment(
        self,
        start_angle,
        end_angle,
        color,
        width
    ):
        # Conversion to Tkinter coordinate system
        start = 90 - end_angle
        extent = end_angle - start_angle

        self.canvas.create_arc(
            self.center_x - self.radius,
            self.center_y - self.radius,
            self.center_x + self.radius,
            self.center_y + self.radius,
            start=start,
            extent=extent,
            style="arc",
            outline=color,
            width=width
        )

    def _draw_tick_mark(self, angle):
        if angle == 0:
            inner_radius = self.radius - 18
            outer_radius = self.radius + 8
            width = 3
        else:
            inner_radius = self.radius - 12
            outer_radius = self.radius + 4
            width = 2

        x1, y1 = self._point_on_arc(angle, inner_radius)
        x2, y2 = self._point_on_arc(angle, outer_radius)

        self.canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            fill=COLORS["text_secondary"],
            width=width
        )

    def _draw_needle(self):
        needle_length = self.radius - 30

        end_x = self.center_x
        end_y = self.center_y - needle_length

        self._needle = self.canvas.create_line(
            self.center_x,
            self.center_y,
            end_x,
            end_y,
            fill=COLORS["meter_needle"],
            width=3,
            arrow="last",
            arrowshape=(10, 12, 4)
        )

        self.canvas.create_oval(
            self.center_x - 10,
            self.center_y - 10,
            self.center_x + 10,
            self.center_y + 10,
            fill=COLORS["meter_needle"],
            outline=""
        )

    def update_deviation(self, cents_deviation):
        if cents_deviation is None:
            self._target_angle = 0.0
        else:
            clamped = max(-50.0, min(50.0, cents_deviation))
            self._target_angle = (clamped / 50.0) * 90.0

        if not self._animation_running:
            self._animation_running = True
            self._animate_needle()

    def _animate_needle(self):
        diff = self._target_angle - self._current_angle

        self._current_angle += diff * 0.20

        self._rotate_needle(self._current_angle)

        if abs(diff) > 0.1:
            self.after(16, self._animate_needle)
        else:
            self._current_angle = self._target_angle
            self._rotate_needle(self._current_angle)
            self._animation_running = False

    def _rotate_needle(self, angle):
        if self._needle is None:
            return

        needle_length = self.radius - 30

        end_x, end_y = self._point_on_arc(
            angle,
            needle_length
        )

        self.canvas.coords(
            self._needle,
            self.center_x,
            self.center_y,
            end_x,
            end_y
        )