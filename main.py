import cv2
import mediapipe as mp
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from datetime import datetime  # For displaying the current time
import platform
import socket

class FaceHandApp(App):
    def build(self):
        # UI layout
        layout = BoxLayout(orientation='vertical')

        # Add a gray background
        with layout.canvas.before:
            Color(0.7, 0.7, 0.7, 0.5)  # Light gray color
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        
        # Ensure the background updates with size and position changes
        layout.bind(size=self._update_rect, pos=self._update_rect)

        # Video display
        self.image = Image()
        layout.add_widget(self.image)

        # Info display
        self.info_label = Label(text="Initializing...", size_hint=(1, 0.1), halign='center', valign='middle')
        layout.add_widget(self.info_label)

        # Open the camera
        self.capture = cv2.VideoCapture(0)

        # MediaPipe for hand detection
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils

        # OpenCV for face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Get system information
        self.system_info = self.get_system_info()

        # Get geographic location
        self.location_info = self.get_ip_info()

        # Schedule the update function to refresh 30 times per second
        Clock.schedule_interval(self.update, 1.0 / 30.0)  # 30 FPS

        return layout

    def _update_rect(self, instance, value):
        """Update background rectangle size and position when window size changes."""
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def get_system_info(self):
        """Retrieve system information such as OS, IP, etc."""
        system_info = {
            'OS': platform.system(),
            'OS_Version': platform.version(),
            'Machine': platform.machine(),
            'Processor': platform.processor(),
            'IP': socket.gethostbyname(socket.gethostname())
        }
        return system_info

    def get_ip_info(self):
        """Retrieve geographic location using the GeoJS API."""
        try:
            response = requests.get("https://get.geojs.io/v1/ip/geo.json")
            return response.json()
        except requests.RequestException:
            return {"country": "Unknown", "city": "Unknown", "ip": "Unknown"}

    def update(self, dt):
        """Capture frames, process hands and faces, and update the UI."""
        ret, frame = self.capture.read()
        if not ret:
            self.info_label.text = "Unable to access the camera!"
            return

        # Detect hands using MediaPipe
        results_hands = self.hands.process(frame)
        if results_hands.multi_hand_landmarks:
            for hand_landmarks in results_hands.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        # Detect faces using OpenCV
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        face_count = 0
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face_count += 1

        # Get the current time
        current_time = datetime.now().strftime("%H:%M:%S")  # Format: HH:MM:SS

        # Update the label with new information
        hand_count = len(results_hands.multi_hand_landmarks) if results_hands.multi_hand_landmarks else 0
        self.info_label.text = f"Faces: {face_count}, Hands: {hand_count}\n" \
                               f"IP: {self.location_info.get('ip', 'Unknown')}\n" \
                               f"Location: {self.location_info.get('city', 'Unknown')}, {self.location_info.get('country', 'Unknown')}\n" \
                               f"OS: {self.system_info['OS']} {self.system_info['OS_Version']}\n" \
                               f"Time: {current_time}\n\n\n\n"

        # Convert the OpenCV frame to a Kivy texture (BGR format)
        buffer = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')  # Use 'bgr'
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture

    def on_stop(self):
        """Release the camera when the app is closed."""
        self.capture.release()


if __name__ == "__main__":
    FaceHandApp().run()
