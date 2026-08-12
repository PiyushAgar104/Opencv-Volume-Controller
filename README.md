# Opencv Finger Volume Controller

A real-time computer vision project that allows you to control your **Windows laptop's system volume using hand gestures**.

The project uses your webcam to track the hand, calculates the distance between the **thumb and index finger**, and maps that distance to the system volume level.

## Features

* Real-time hand tracking
* Thumb and index finger distance detection
* Gesture-based volume control
* Direct Windows system volume control
* Real-time volume percentage
* Visual volume bar
* Hand landmark visualization
* Webcam-based interaction
* Simple and lightweight interface

## How It Works

The system follows a simple computer vision pipeline:

```text
Webcam
   ↓
Hand Detection
   ↓
MediaPipe Hand Landmarks
   ↓
Thumb + Index Finger
   ↓
Distance Calculation
   ↓
Distance → Volume %
   ↓
Windows System Volume
```

### Gesture Control

```text
Thumb + Index Close
        ↓
   Volume Down

Thumb + Index Far
        ↓
   Volume Up
```

The distance between landmark **4 (thumb tip)** and landmark **8 (index finger tip)** is used to determine the volume level.

## Technologies Used

* **Python**
* **OpenCV** — Webcam capture and real-time image processing
* **MediaPipe** — Hand landmark detection
* **Pycaw** — Windows system audio control
* **NumPy** — Numerical operations

## Project Structure

```text
FingerVolumeController/
│
├── main.py
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/FingerVolumeController.git
```

```bash
cd FingerVolumeController
```

### 2. Install dependencies

```bash
pip install opencv-python mediapipe==0.10.21 pycaw comtypes numpy
```

### 3. Run the project

```bash
python main.py
```

Make sure your webcam is connected and accessible.

## Controls

| Gesture / Key       | Action           |
| ------------------- | ---------------- |
| Thumb + Index close | Decrease volume  |
| Thumb + Index far   | Increase volume  |
| `Q`                 | Exit application |

## Volume Mapping

The project maps the detected finger distance to a volume range:

```text
Minimum Distance  →  0% Volume
        ↓
   Finger Distance
        ↓
Maximum Distance  →  100% Volume
```

The mapped value is then converted into the Windows audio endpoint's volume range using Pycaw.

## Requirements

* Windows OS
* Python 3.x
* Working webcam
* Microphone/camera permissions enabled
* Internet connection for initial package installation

## Example

When the thumb and index finger are close:

```text
🤏
Volume ↓
```

When the fingers are separated:

```text
👍        ☝
   ← → 
Volume ↑
```

## Future Improvements

* Smooth volume transitions
* Mute gesture
* Play/Pause gesture
* Two-hand gesture controls
* Media playback controls
* Custom gesture recognition
* Better UI and animations
* FPS monitoring
* Gesture-based brightness control

## Learning Outcomes

Through this project, I explored:

* Real-time computer vision
* Hand landmark detection
* Coordinate-based gesture recognition
* Distance measurement between landmarks
* Mapping physical gestures to numerical values
* Controlling Windows system APIs using Python

## License

This project is open-source and available for learning and experimentation.

---

**Built with Python, OpenCV, MediaPipe and Pycaw.**
