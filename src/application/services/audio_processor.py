# Audio processor service that continuously captures and processes audio
# Runs in a separate thread to avoid blocking the UI

import threading
import time
from typing import Callable, Optional

from src.domain.entities.note import Note
from src.domain.interfaces.audio_capture import AudioCaptureProtocol
from src.application.use_cases.tune_guitar import TuneGuitarUseCase

# Type alias for the callback function
NoteCallback = Callable[[Optional[Note]], None]

class AudioProcessorService:
    def __init__(
            self,
            audio_capture: AudioCaptureProtocol,
            tune_guitar_use_case: TuneGuitarUseCase,
    ):
        # Initialize the audio processor service
        self._audio_capture = audio_capture         # Implementation of AudioCaptureProtocol
        self._tune_guitar = tune_guitar_use_case    # Use case for tuning detection

        self._running = False
        self._processing_thread: Optional[threading.Thread] = None
        self._callbacks: list[NoteCallback] = []
        self._lock = threading.Lock()
    
    def register_callback(self, callback: NoteCallback) -> None:
        # Register a callback to be notified when a new note is detected
        with self._lock:
            if callback not in self._callbacks:
                self._callbacks.append(callback)
    
    def unregister_callback(self, callback: NoteCallback) -> None:
        # Unregister a previously registered callback
        with self._lock:
            if callback in self._callbacks:
                self._callbacks.remove(callback)
    
    def _notify_callbacks(self, note: Optional[Note]) -> None:
        # Notify all registered callbacks with the detected note
        with self._lock:
            callbacks_copy = self._callbacks.copy()
        
        for callback in callbacks_copy:
            try:
                callback(note)
            except Exception as e:
                print(f"Error in callback: {e}")
    
    def _processing_loop(self) -> None:
        # Main processing loop that runs in a separate thread
        # Continuously captures audio and processes it
        while self._running:
            try:
                # Get audio block from capture
                audio_data = self._audio_capture.get_audio_block(timeout=0.1)

                if audio_data is not None:
                    # Process the audio to detect a note
                    note = self._tune_guitar.execute(audio_data)
                    # Notify callbacks with the result
                    self._notify_callbacks(note)
                else:
                    # No audio data available, notify with None
                    self._notify_callbacks(None)
            except Exception as e:
                print(f"Error in processing loop: {e}")
                # Small delay to avoid tight loop on errors
                time.sleep(0.1)
    
    def start(self) -> None:
        # Start the audio processor service
        # Begins capturing and processing the audio in a separate thread
        if self._running:
            print("Audio processor already running")
            return
        
        # Start the audio capture
        try:
            self._audio_capture.start()
        except Exception as e:
            raise RuntimeError(f"Failed to start audio capture: {e}")
        
        # Start the processing thread
        self._running = True
        self._processing_thread = threading.Thread(
            target=self._processing_loop,
            daemon=True,
            name="AudioProcessorThread"
        )
        self._processing_thread.start()
        print("Audio processor started")
    
    def stop(self) -> None:
        # Stop the audio processor service
        # Stops capturing and processing audio
        if not self._running:
            print("Audio processor not running")
            return
        
        # Signal the processing loop to stop
        self._running = False

        # Wait for the processing thread to finish
        if self._processing_thread and self._processing_thread.is_alive():
            self._processing_thread.join(timeout=2.0)
        
        # Stop the audio capture
        try:
            self._audio_capture.stop()
        except Exception as e:
            print(f"Error stopping audio capture: {e}")
        
        print("Audio processor stopped")
    
    @property
    def _is_running(self) -> bool:
        # Check if the audio processor is currently running
        return self._running