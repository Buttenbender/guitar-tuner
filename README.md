# 🎸 Guitar Tuner
A lightweight and efficient desktop application built with Python to help you tune your guitar.
It uses real-time audio analysis to detect the pitch of the notes you play and provides visual
feedback to help you get perfectly in tune.
## Author
- João Büttenbender
## ✨ Features
- **Real-time Audio Capture:** Listens to your instrument via microphone with low latency
- **Chromatic Mode:** Detects any note being played and indicates if it is sharp, flat or in tune
- **Dark Mode Interface:** Modern, eye-friendly dark theme designed for confort
- **Lightweight:** Optimized to run smoothly without consuming excessive system resources
# 🛠️ Technologies Used
- **Python 3.11**
- **Librosa:** For pitch detection and audio analysis
- **SoundDevice:** For real-time microphone input capture
- **CustomTkinter:** For the modern desktop graphical user interface (GUI)
- **NumPy:** For numerical operations and audio data processing
# 📋 Prerequisites
Before you begin, ensure you have met the following requirements:
- **Python 3.8+** installed on your machine
- A working **microphone** connected to your computer
- **Windows 11** (Optimized for this environment, though may work on others)
# 🚀 Installation
1. Clone this repository or download the source code
2. Open your terminal or command prompt in the project folder
3. Create and activate a virtual environment:
```
python -m venv venv
```
```
venv\Scripts\Activate.ps1
```
4. Install dependencies:
```
pip install -r requirements.txt
```
5. Run:
```
python main.py
```
