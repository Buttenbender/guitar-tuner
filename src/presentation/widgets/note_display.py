# Note display widget - shows the detected note, octave, frequency and cents

import customtkinter as ctk

from src.domain.entities.note import Note, TuningStatus
from src.infrastructure.config.constants import COLORS

class NoteDisplay(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        # Initialize the note display widget
        super().__init__(master, fg_color=COLORS['surface'], **kwargs)

        # Note name (large)
        self.note_label = ctk.CTkLabel(
            self,
            text="--",
            font=ctk.CTkFont(size=72, weight="bold"),
            text_color=COLORS['text_primary']
        )
        self.note_label.pack(pady=(20, 5))

        # Octave number
        self.octave_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=24),
            text_color=COLORS['text_secondary']
        )
        self.octave_label.pack(pady=(0, 10))
        
        # Frequency in Hz
        self.frequency_label = ctk.CTkLabel(
            self,
            text="-- Hz",
            font=ctk.CTkFont(size=18),
            text_color=COLORS['text_secondary']
        )
        self.frequency_label.pack(pady=5)
        
        # Cents deviation
        self.cents_label = ctk.CTkLabel(
            self,
            text="-- cents",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLORS['text_secondary']
        )
        self.cents_label.pack(pady=5)
    
    def update_note(self, note: Note | None):
        # Update the display with a new note
        if note is None:
            self._clear_display()
            return
        
        # Update note name
        self.note_label.configure(text=note.name)
        
        # Update octave
        self.octave_label.configure(text=f"Octave {note.octave}")
        
        # Update frequency
        if note.detected_frequency is not None:
            self.frequency_label.configure(text=f"{note.detected_frequency:.1f} Hz")
        else:
            self.frequency_label.configure(text="-- Hz")
        
        # Update cents deviation
        if note.cents_deviation is not None:
            cents_text = f"{note.cents_deviation:+.1f} cents"
            self.cents_label.configure(text=cents_text)
            
            # Color based on tuning status
            status = note.get_tuning_status()
            color = self._get_color_for_status(status)
            self.cents_label.configure(text_color=color)
            self.note_label.configure(text_color=color)
        else:
            self.cents_label.configure(text="-- cents")
            self.cents_label.configure(text_color=COLORS['text_secondary'])
            self.note_label.configure(text_color=COLORS['text_primary'])
    
    def _clear_display(self):
        # Clear all display elements
        self.note_label.configure(text="--", text_color=COLORS['text_primary'])
        self.octave_label.configure(text="")
        self.frequency_label.configure(text="-- Hz")
        self.cents_label.configure(text="-- cents", text_color=COLORS['text_secondary'])
    
    def _get_color_for_status(self, status: TuningStatus) -> str:
        # Get the color for a tuning status
        if status == TuningStatus.PERFECT:
            return COLORS['perfect']
        elif status == TuningStatus.SLIGHTLY_OFF:
            return COLORS['slightly_off']
        else:
            return COLORS['very_off']