# Main window of the guitar tuner application

import customtkinter as ctk

from src.presentation.widgets.meter_widget import MeterWidget
from src.presentation.widgets.note_display import NoteDisplay
from src.infrastructure.config.constants import COLORS

class MainWindow(ctk.CTk):
    def __init__(self):
        # Initialize the main window
        super().__init__()
        
        # Window configuration
        self.title("Guitar Tuner")
        self.geometry("500x700")
        self.resizable(False, False)
        
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Configure window background
        self.configure(fg_color=COLORS['background'])
        
        # Title label
        self.title_label = ctk.CTkLabel(
            self,
            text="🎸 Guitar Tuner",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COLORS['text_primary']
        )
        self.title_label.pack(pady=(20, 10))
        
        # Note display widget
        self.note_display = NoteDisplay(self)
        self.note_display.pack(pady=10, padx=20, fill="x")
        
        # Meter widget
        self.meter = MeterWidget(self)
        self.meter.pack(pady=10, padx=20)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self,
            text="Listening...",
            font=ctk.CTkFont(size=14),
            text_color=COLORS['text_secondary']
        )
        self.status_label.pack(pady=20)
    
    def update_status(self, message: str):
        # Update the status message at the bottom of the window
        self.status_label.configure(text=message)