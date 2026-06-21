# Pitch detector interface definition
# Defines the contract for pitch detection implementations

from abc import ABC, abstractmethod
from typing import Optional
import numpy as np

from src.domain.entities.pitch import Pitch

class PitchDetectorProtocol(ABC):
    @abstractmethod
    def detect(self, audio_data: np.ndarray, sample_rate: int) -> Optional[Pitch]:
        # Detect the fundamental frequency (pitch) in the given audio data
        pass

    @abstractmethod
    def get_sample_rate(self) -> int:
        # Get the expected sample rate for this pitch detector
        pass