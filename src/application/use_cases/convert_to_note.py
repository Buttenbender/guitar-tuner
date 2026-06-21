# Use case for converting a detected pitch to a musical note

import math
from typing import Optional, Tuple

from src.domain.entities.note import Note
from src.domain.entities.pitch import Pitch
from src.infrastructure.config.constants import NOTE_FREQUENCIES, NOTE_NAMES

class ConvertToNoteUseCase:
    def execute(self, pitch: Pitch) -> Optional[Note]:
        # Convert a detected pitch to the closest musical note
        if pitch is None:
            return None
        
        # Find the closest note
        note_name, octave, theoretical_freq = self._find_closest_note(pitch.frequency)

        if note_name is None:
            return None
        
        # Calculate cents deviation
        cents_deviation = self._calculate_cents_deviation(
            pitch.frequency, theoretical_freq
        )

        return Note(
            name=note_name,
            octave=octave,
            theoretical_frequency=theoretical_freq,
            detected_frequency=pitch.frequency,
            cents_deviation=cents_deviation,
        )
    
    def _find_closest_note(self, frequency: float) -> Tuple[Optional[str], int, float]:
        # Find the closest note to the given frequency
        min_distance = float('inf')
        closest_note = None
        closest_octave = 0
        closest_freq = 0.0

        for full_note, theoretical_freq in NOTE_FREQUENCIES.items():
            # Extract note name and octave from full note
            note_name, octave = self._parse_note(full_note)

            # Calculate distance in cents (logarithmic scale)
            if frequency > 0 and theoretical_freq > 0:
                distance = abs(1200 * math.log2(frequency / theoretical_freq))

                if distance < min_distance:
                    min_distance = distance
                    closest_note = note_name
                    closest_octave = octave
                    closest_freq = theoretical_freq

        return closest_note, closest_octave, closest_freq
    
    def _parse_note(self, full_note: str) -> Tuple[str, int]:
        # Parse a full note string into name and octave

        # Find where the octave number starts
        for i, char in enumerate(full_note):
            if char.isdigit():
                note_name = full_note[:i]
                octave = int(full_note[i:])
                return note_name, octave
        
        raise ValueError(f"Invalid note format: {full_note}")
    
    def _calculate_cents_deviation(
            self, detected_freq: float, theoretical_freq: float
    ) -> float:
        # Calculate the deviation in cents between detected and theoretical frequency
        if detected_freq <= 0 or theoretical_freq <= 0:
            return 0.0
        
        cents = 1200 * math.log2(detected_freq / theoretical_freq)

        # Clamp to [-50, +50] range (half a semitone in each direction)
        return max(-50.0, min(50.0, cents))