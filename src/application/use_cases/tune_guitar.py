# Main use case that orchestrates the complete guitar tuning process

from typing import Optional
import numpy as np

from src.domain.entities.note import Note
from src.application.use_cases.detect_pitch import DetectPitchUseCase
from src.application.use_cases.convert_to_note import ConvertToNoteUseCase
from src.infrastructure.config.constants import MIN_CONFIDENCE

class TuneGuitarUseCase:
    def __init__(
            self, 
            detect_pitch_use_case: DetectPitchUseCase,
            convert_to_note_use_case: ConvertToNoteUseCase,
            min_confidence: float = MIN_CONFIDENCE,
    ):
        # Initialize the use case with its dependencies
        self._detect_pitch = detect_pitch_use_case          # Use case for pitch detection
        self._convert_to_note = convert_to_note_use_case    # Use case for note conversion
        self._min_confidence = min_confidence               # Minimum confidence threshold to accept a detection
    
    def execute(self, audio_data: np.ndarray) -> Optional[Note]:
        # Execute the complete tuning process on a block of audio data

        # Step 1: Detect pitch
        pitch = self._detect_pitch.execute(audio_data)

        if pitch is None:
            return None
        
        # Step 2: Check confidence
        if not pitch.is_reliable(self._min_confidence):
            return None
        
        # Step 3: Convert to note
        note = self._convert_to_note.execute(pitch)

        return note