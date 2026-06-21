# Note entity - represents a musical note with tuning information

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from src.domain.entities.pitch import Pitch
from src.infrastructure.config.constants import NOTE_FREQUENCIES, TUNING_THRESHOLDS

class TuningStatus(Enum):
    # Enumeration of tuning status for a note
    PERFECT = "perfect"
    SLIGHTLY_OFF = "slightly_off"
    VERY_OFF = "very_off"

@dataclass(frozen=True)
class Note:
    name: str                                   # Note name
    octave: int                                 # Octave number
    theoretical_frequency: float                # Exact frequency this note should have
    detected_frequency: Optional[float] = None  # Actual detected frequency (Hz) if available
    cents_deviation: Optional[float] = None     # Deviation from theoretical frequency in cents

    def __post_init__(self):
        # Validate note data after initialization
        if self.theoretical_frequency <= 0:
            raise ValueError(f"Theoretical frequency must be positive, got {self.theoretical_frequency}")
        
        if self.cents_deviation is not None:
            if not -100 <= self.cents_deviation <= 100:
                raise ValueError(f"Cents deviation must be between -100 and 100, got {self.cents_deviation}")

    @property
    def full_name(self) -> str:
        # Get the full name with octave
        return f"{self.name}{self.octave}"
    
    @property
    def is_in_tune(self) -> bool:
        # Check if the note is perfectly in tune (within ~5 cents)
        if self.cents_deviation is None:
            return False
        return abs(self.cents_deviation) <= TUNING_THRESHOLDS['perfect']
    
    def get_tuning_status(self) -> TuningStatus:
        # Get the tuning status of this note
        if self.cents_deviation is None:
            return TuningStatus.VERY_OFF
        
        abs_deviation = abs(self.cents_deviation)

        if abs_deviation <= TUNING_THRESHOLDS['perfect']:
            return TuningStatus.PERFECT
        elif abs_deviation <= TUNING_THRESHOLDS['slightly_off']:
            return TuningStatus.SLIGHTLY_OFF
        else:
            return TuningStatus.VERY_OFF
    
    def is_sharp(self) -> bool:
        # Check if the note is sharp (higher than it should be)
        if self.cents_deviation is None:
            return False
        return self.cents_deviation > 0
    
    def is_flat(self) -> bool:
        # Check if the note is flat (lower than it should be)
        if self.cents_deviation is None:
            return False
        return self.cents_deviation < 0
    
    def __str__(self) -> str:
        # String representation for debugging
        if self.cents_deviation is not None:
            return f"Note({self.full_name}, {self.detected_frequency:.2f}Hz, {self.cents_deviation:+.1f} cents)"
        return f"Note({self.full_name}, {self.theoretical_frequency:.2f}Hz)"