# Face and Hand Detection App

This project is a Python application that uses computer vision to detect faces and hands in real-time via a webcam. It leverages OpenCV, MediaPipe, and Kivy to provide a graphical interface and visual detection capabilities.

> **Disclaimer:** This application is for educational and personal use only. Ensure you comply with privacy laws and have explicit permission before using it.

---

## Features
- Detects hands using MediaPipe's Hand module.
- Detects faces using OpenCV's Haar Cascade.
- Displays system information, including OS details and IP address.
- Shows geographic location based on IP using the GeoJS API.
- Real-time video feed with overlaid detection boxes and labels.

---

## Requirements
- Python 3.7+
- A webcam

---

## Installation

1. Clone the repository or copy the script to your local machine.
2. Install the required Python packages:

```bash
pip install opencv-python mediapipe kivy requests
```

3. Ensure you have the necessary OpenCV Haar Cascade XML file:
   - `haarcascade_frontalface_default.xml` (already included with OpenCV).

---

## Usage

1. Run the script:

```bash
python face_hand_app.py
```

2. The application will:
   - Open a Kivy window with a video feed.
   - Detect and highlight faces and hands in real-time.
   - Display system and geographic information, including:
     - Face and hand counts
     - Current time
     - IP address and approximate location
     - Operating system details

---

## Output

### Real-Time Information
- The app displays:
  - The number of detected faces and hands.
  - Current time (updated live).
  - Geographic location based on IP.
  - System details (e.g., OS version, IP address).

### Visual Output
- The video feed includes:
  - Bounding boxes around detected faces.
  - Hand landmarks connected with lines for detected hands.

---

## Code Highlights

- **Face Detection**: Utilizes OpenCV's `CascadeClassifier` for efficient face detection.
- **Hand Detection**: Employs MediaPipe's `Hands` solution for accurate hand tracking and landmark detection.
- **Kivy UI**: Provides a simple GUI for displaying the video feed and information overlays.
- **System and Location Info**:
  - System info is retrieved using Python's `platform` and `socket` modules.
  - Geographic info is fetched from the GeoJS API.

---

## Dependencies
- [OpenCV](https://opencv.org/)
- [MediaPipe](https://mediapipe.dev/)
- [Kivy](https://kivy.org/)
- [Requests](https://pypi.org/project/requests/)

---

## Notes
1. Ensure your webcam is connected and accessible.
2. The app uses the GeoJS API for location data. If the API is unreachable, location information will display as "Unknown."
3. Adjust detection thresholds in the code as needed for different environments or lighting conditions.

---

## License
This project is open-source and distributed under the MIT License. See the `LICENSE` file for more information.

---

**Disclaimer:** Ensure compliance with privacy regulations when using this app, especially in public or sensitive environments.

