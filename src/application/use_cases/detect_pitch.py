# Use case for detecting pitch from audio data

from typing import Optional
import numpy as np

from src.domain.entities.pitch import Pitch
from src.domain.interfaces.pitch_detector import PitchDetectorProtocol

class DetectPitchUseCase:
    def __init__(self, pitch_detector: PitchDetectorProtocol):
        # Initialize the use case with a pitch detector implementation
        self._pitch_detector = pitch_detector
    
    def execute(self, audio_data: np.ndarray) -> Optional[Pitch]:
        # Execute the pitch detection on the given audio data
        if audio_data is None or len(audio_data) == 0:
            return None
        
        # Flatten the audio data in case it has shape (N, 1)
        if audio_data.ndim > 1:
            audio_data = audio_data.flatten()

        # Delegate to the pitch detector implementation
        sample_rate = self._pitch_detector.get_sample_rate()
        return self._pitch_detector.detect(audio_data, sample_rate)