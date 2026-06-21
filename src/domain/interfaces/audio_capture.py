# Audio capture interface definition
# Defines the contract for audio capture implementations

from abc import ABC, abstractmethod
from typing import Optional
import numpy as np

class AudioCaptureProtocol(ABC):
    @abstractmethod
    def start(self) -> None:
        # Start audio capture
        # Should initialize resources and begin capturing audio in a separate thread
        pass

    @abstractmethod
    def stop(self) -> None:
        # Stop audio capture and clean up resources
        # Should be safe to call multiple times
        pass

    @abstractmethod
    def get_audio_block(self, timeout: float = 0.1) -> Optional[np.ndarray]:
        # Get the next audio block from the capture queue
        pass

    @abstractmethod
    def is_available(self) -> None:
        # Check if audio capture is available on the system
        pass

    @abstractmethod
    def is_running(self) -> None:
        # Check if audio capture is currently running
        pass