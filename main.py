# Guitar Tuner - Main application entry point

import customtkinter as ctk

# Infrastructure imports
from src.infrastructure.audio.sounddevice_capture import SoundDeviceAudioCapture
from src.infrastructure.pitch_detection.librosa_detector import LibrosaPitchDetector

# Application imports
from src.application.use_cases.detect_pitch import DetectPitchUseCase
from src.application.use_cases.convert_to_note import ConvertToNoteUseCase
from src.application.use_cases.tune_guitar import TuneGuitarUseCase
from src.application.services.audio_processor import AudioProcessorService

# Presentation imports
from src.presentation.views.main_window import MainWindow
from src.presentation.controllers.tuner_controller import TunerController

def create_application() -> tuple[MainWindow, TunerController]:
    # Create and wire together all application components
    # This function implements the Dependency Injection pattern,
    # creating all instances in the correct order and injecting dependencies
    print("Initializing Guitar Tuner...")
    
    # Step 1: Create infrastructure implementations
    print("  - Creating audio capture (sounddevice)...")
    audio_capture = SoundDeviceAudioCapture()
    
    print("  - Creating pitch detector (librosa)...")
    pitch_detector = LibrosaPitchDetector()
    
    # Step 2: Create use cases
    print("  - Creating use cases...")
    detect_pitch_use_case = DetectPitchUseCase(pitch_detector)
    convert_to_note_use_case = ConvertToNoteUseCase()
    tune_guitar_use_case = TuneGuitarUseCase(
        detect_pitch_use_case,
        convert_to_note_use_case
    )
    
    # Step 3: Create application services
    print("  - Creating audio processor service...")
    audio_processor = AudioProcessorService(
        audio_capture,
        tune_guitar_use_case
    )
    
    # Step 4: Create presentation layer
    print("  - Creating UI...")
    main_window = MainWindow()
    
    # Step 5: Create controller and wire everything together
    print("  - Creating controller...")
    controller = TunerController(main_window, audio_processor)
    
    print("Initialization complete!")
    
    return main_window, controller

def main():
    # Main function that starts the guitar tuner application
    try:
        # Create the application
        main_window, controller = create_application()
        
        # Set up window close handler
        main_window.protocol("WM_DELETE_WINDOW", controller.on_closing)
        
        # Start the audio processor
        controller.start()
        
        # Start the main UI loop
        print("\nStarting Guitar Tuner...")
        print("Play a note on your guitar to see the tuning!")
        print("Press Ctrl+C or close the window to exit.\n")
        
        main_window.mainloop()
        
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        controller.stop()
    except Exception as e:
        print(f"\nError starting application: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())