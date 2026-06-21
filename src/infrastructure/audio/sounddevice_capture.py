# Sounddevice implementation of AudioCaptureProtocol
# Handles real-time audio capture from microphone using the sounddevice library

import threading
import queue
import numpy as np
import sounddevice as sd

from src.domain.interfaces.audio_capture import AudioCaptureProtocol
from src.infrastructure.config.constants import SAMPLE_RATE, BLOCK_SIZE, CHANNELS

class SoundDeviceAudioCapture(AudioCaptureProtocol):
    def __init__(
            self,
            sample_rate: int = SAMPLE_RATE,
            block_size: int = BLOCK_SIZE,
            channels: int = CHANNELS,
    ):
        # Initialize the audio capture with configuration parameters
        self._sample_rate = sample_rate     # Audio sample rate in Hz (default: 44100)
        self._block_size = block_size       # Number of samples per audio block (default: 2048)
        self._channels = channels           # Number of audio channels (default: 1 for mono)

        self._audio_queue: queue.Queue = queue.Queue()
        self._is_running_flag = False
        self._stream: sd.InputStream | None = None
        self._capture_thread: threading.Thread | None = None
        self._lock = threading.Lock()
    
    def _audio_callback(
            self,
            indata: np.ndarray,
            frames: int,
            time_info: object,
            status: sd.CallbackFlags
    ) -> None:
        # Callback function called by sounddevice for each audio block
        if status:
            print(f"Audio callback status: {status}")
        
        # Copy the audio data and put it in the queue
        # We copy because the indata might be reused by sounddevice
        audio_data = indata.copy()

        # If queue is getting full, remove oldest items to prevent memory issues
        if self._audio_queue.qsize() > 10:
            try:
                self._audio_queue.get_nowait()
            except queue.Empty:
                pass
        
        self._audio_queue.put(audio_data)
    
    def _capture_loop(self) -> None:
        # Main capture loop that runs in a separate thread
        # Keeps the audio stream open while is_running is True
        try:
            # Open audio stream with callback
            with sd.InputStream(
                samplerate=self._sample_rate,
                blocksize=self._block_size,
                channels=self._channels,
                callback=self._audio_callback,
                dtype='float32'
            ) as stream:
                with self._lock:
                    self._stream = stream
                
                # Keep the stream open while running
                while self._is_running_flag:
                    sd.sleep(100)   # Small sleep to avoid busy waiting
        except Exception as e:
            print(f"Error in audio capture: {e}")
            with self._lock:
                self._is_running_flag = False
    
    def start(self) -> None:
        # Start audio capture in a separate thread
        with self._lock:
            if self._is_running_flag:
                print("Audio capture already running")
                return
        
        # Check if microphone is available
        if not self.is_available():
            raise RuntimeError("No microphone available on the system")
        
        with self._lock:
            self._is_running_flag = True
        
        # Create and start the capture thread
        self._capture_thread = threading.Thread(
            target=self._capture_loop,
            daemon=True,
            name="AudioCaptureThread"
        )
        self._capture_thread.start()
        print("Audio capture started")
    
    def stop(self) -> None:
        # Stop the audio capture and clean up resources
        with self._lock:
            if not self._is_running_flag:
                print("Audio capture not running")
                return
            
            self._is_running_flag = False
        
        # Wait for the thread to finish
        if self._capture_thread and self._capture_thread.is_alive():
            self._capture_thread.join(timeout=1.0)
        
        # Clear queue
        while not self._audio_queue.empty():
            try:
                self._audio_queue.get_nowait()
            except queue.Empty:
                break
        
        with self._lock:
            self._stream = None
        
        print("Audio capture stopped")
    
    def get_audio_block(self, timeout: float = 0.1) -> np.ndarray | None:
        # Get the next audio block from the queue
        try:
            return self._audio_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def is_available(self) -> bool:
        # Check if a microphone is available on the system
        try:
            # Try to get default input device
            device_info = sd.query_devices(kind='input')
            return device_info is not None and device_info['max_input_channels'] > 0
        except Exception:
            return False
    
    def is_running(self) -> bool:
        # Check if audio capture is currently running
        with self._lock:
            return self._is_running_flag
    
    @property
    def sample_rate(self) -> int:
        # Get the sample rate being used
        return self._sample_rate
    
    @property
    def block_size(self) -> int:
        # Get the block size being used
        return self._block_size