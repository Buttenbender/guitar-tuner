# Pitch entity - represents a detected fundamental frequency

from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Pitch:
    frequency: float        # Fundamental frequency in Hz
    confidence: float       # Confidence level of the detection (0.0 to 1.0)

    def __post_init__(self):
        # Validate the pitch data after initialization
        if self.frequency <= 0:
            raise ValueError(f"Frequency must be positive, got {self.frequency}")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"Confidence must be between 0.0 and 1.0, got {self.confidence}")
    
    def is_reliable(self, min_confidence: float = 0.5) -> bool:
        # Check if this pitch detection is reliable enough to use
        return self.confidence >= min_confidence
    
    def __str__(self) -> str:
        # String representation for debugging
        return f"Pitch({self.frequency:.2f} Hz, confidence={self.confidence:.2f})"