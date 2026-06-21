# Tuner controller - mediates between UI and application layer

from typing import Optional

from src.domain.entities.note import Note
from src.application.services.audio_processor import AudioProcessorService
from src.presentation.views.main_window import MainWindow

class TunerController:
    def __init__(
            self,
            view: MainWindow,
            audio_processor: AudioProcessorService,
    ):
        # Initialize the tuner controller
        self._view = view
        self._audio_processor = audio_processor

        # Register callback to receive note updates
        self._audio_processor.register_callback(self._on_note_detected)
    
    def _on_note_detected(self, note: Optional[Note]) -> None:
        # Callback invoked when a new note is detected
        # Updates the UI with the new note information

        # Update note display
        self._view.note_display.update_note(note)
        
        # Update meter
        if note is not None and note.cents_deviation is not None:
            self._view.meter.update_deviation(note.cents_deviation)
        else:
            self._view.meter.update_deviation(None)
        
    def start(self) -> None:
        # Start the audio processor and begin listening
        try:
            self._audio_processor.start()
            self._view.update_status("Listening...")
        except RuntimeError as e:
            self._view.update_status(f"Error: {e}")
    
    def stop(self) -> None:
        # Stop the audio processor
        self._audio_processor.stop()
        self._view.update_status("Stopped")
    
    def on_closing(self) -> None:
        # Handle window closing event
        # Cleans up resources before the application exits
        self.stop()
        self._view.destroy()