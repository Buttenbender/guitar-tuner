# Librosa implementation of PitchDetectorProtocol
# Uses the probabilistic YIN (pYIN) algorithm for pitch detection

import numpy as np
import librosa

from src.domain.entities.pitch import Pitch
from src.domain.interfaces.pitch_detector import PitchDetectorProtocol
from src.infrastructure.config.constants import SAMPLE_RATE

class LibrosaPitchDetector(PitchDetectorProtocol):
    def __init__(
            self,
            sample_rate: int = SAMPLE_RATE,
            fmin: float = 60.0,
            fmax: float = 1000.0,
    ):
        # Initialize the librosa pitch detector
        self._sample_rate = sample_rate     # Expected sample rate for audio data (default: 44100)
        self._fmin = fmin                    # Minimum frequency to detect in Hz
        self._fmax = fmax                    # Maximum frequency to detect in Hz
    
    def detect(self, audio_data: np.ndarray, sample_rate: int) -> Pitch | None:
        # Detect the fundamental frequency (pitch) in the given audio data
        # Uses librosa's pYIN algorithm which provides both frequency and voiced probability (confidence)

        # Validate input
        if audio_data is None or len(audio_data) == 0:
            return None
        
        # Ensure we have enough samples for analysis
        if len(audio_data) < 2048:
            return None
        
        try:
            # Use pYIN algorithm for pitch detection
            # pYIN returns: f0 (fundamental frequencies), voiced_flag, voiced_probs
            f0, voiced_flag, voiced_probs = librosa.pyin(
                y=audio_data,
                fmin=self._fmin,
                fmax=self._fmax,
                sr=sample_rate,
                fill_na=None        # Return NaN for unvoiced frames
            )

            # Filter out NaN values (unvoiced frames)
            valid_indices = ~np.isnan(f0)
            if not np.any(valid_indices):
                return None
            
            # Get valid frequencies and their probabilities
            valid_f0 = f0[valid_indices]
            valid_probs = voiced_probs[valid_indices]

            # Use the frame with highest confidence
            best_index = np.argmax(valid_probs)
            best_frequency = valid_f0[best_index]
            best_confidence = valid_probs[best_index]

            # Validate the results
            if best_frequency <= 0 or best_confidence < 0:
                return None
            
            return Pitch(
                frequency=float(best_frequency),
                confidence=float(best_confidence)
            )
        
        except Exception as e:
            print(f"Error in pitch detection: {e}")
            return None
    
    def get_sample_rate(self) -> int:
        # Get the expected sample rate for this pitch detector
        return self._sample_rate
    
    @property
    def fmin(self) -> float:
        # Get the minimum detectable frequency
        return self._fmin
    
    @property
    def fmax(self) -> float:
        # Get the maximum detectable frequency
        return self._fmax