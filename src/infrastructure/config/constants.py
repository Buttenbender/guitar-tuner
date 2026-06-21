# Constants and configuration for the guitar tuner application

# Audio configuration
SAMPLE_RATE = 44100     # Hz - standart audio sample rate
BLOCK_SIZE = 2048       # Number of samples per audio block
CHANNELS = 1            # Mono audio (single channel)

# Muscal note frequencies (A4 = 440Hz standart tuning)
NOTE_FREQUENCIES = {
    # Octave 2 (low E string)
    'E2': 82.41,
    'F2': 87.31,
    'F#2': 92.50,
    'G2': 98.00,
    'G#2': 103.83,
    'A2': 110.00,
    'A#2': 116.54,
    'B2': 123.47,
    
    # Octave 3 (A and D strings)
    'C3': 130.81,
    'C#3': 138.59,
    'D3': 146.83,
    'D#3': 155.56,
    'E3': 164.81,
    'F3': 174.61,
    'F#3': 185.00,
    'G3': 196.00,
    'G#3': 207.65,
    'A3': 220.00,
    'A#3': 233.08,
    'B3': 246.94,
    
    # Octave 4 (G, B, and high E strings)
    'C4': 261.63,
    'C#4': 277.18,
    'D4': 293.66,
    'D#4': 311.13,
    'E4': 329.63,
    'F4': 349.23,
    'F#4': 369.99,
    'G4': 392.00,
    'G#4': 415.30,
    'A4': 440.00,  # Reference frequency
    'A#4': 466.16,
    'B4': 493.88,
    
    # Octave 5 (high notes)
    'C5': 523.25,
    'C#5': 554.37,
    'D5': 587.33,
    'D#5': 622.25,
    'E5': 659.25,
    'F5': 698.46,
    'F#5': 739.99,
    'G5': 783.99,
    'G#5': 830.61,
    'A5': 880.00,
    'A#5': 932.33,
    'B5': 987.77,
}

# Note names in order (for chromatic scale)
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Cents thresholds for tuning classification
# 100 cents = 1 semitone
TUNING_THRESHOLDS = {
    'perfect': 5,      # ~5 cents or less = perfectly in tune
    'slightly_off': 15, # ~15 cents = slightly off
    # More than ~15 cents = very off
}

# UI Colors (Dark Theme)
COLORS = {
    'background': '#1a1a1a',
    'surface': '#2d2d2d',
    'text_primary': '#ffffff',
    'text_secondary': '#b0b0b0',
    'accent': '#4a9eff',
    
    # Tuning indicator colors
    'perfect': '#4caf50',      # Green - in tune
    'slightly_off': '#ff9800', # Orange - slightly off
    'very_off': '#f44336',     # Red - very off
    
    # Meter colors
    'meter_background': '#3d3d3d',
    'meter_needle': '#ffffff',
}

# UI Dimensions
METER_WIDTH = 400
METER_HEIGHT = 250
NEEDLE_LENGTH = 180

# Update intervals
UI_UPDATE_INTERVAL = 50  # ms - how often to update the UI

# Pitch detection configuration
MIN_CONFIDENCE = 0.5  # Minimum confidence to accept a pitch detection