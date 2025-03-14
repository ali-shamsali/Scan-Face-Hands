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
from datetime import datetime
import platform
import socket
from deepface import DeepFace

class FaceHandEmotionApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        
        with layout.canvas.before:
            Color(0.7, 0.7, 0.7, 0.5)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        
        layout.bind(size=self._update_rect, pos=self._update_rect)

        self.image = Image()
        layout.add_widget(self.image)

        self.info_label = Label(text="Initializing...", size_hint=(1, 0.1), halign='center', valign='middle')
        layout.add_widget(self.info_label)

        self.capture = cv2.VideoCapture(0)

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        self.system_info = self.get_system_info()
        self.location_info = self.get_ip_info()

        Clock.schedule_interval(self.update, 1.0 / 30.0)

        return layout

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def get_system_info(self):
        system_info = {
            'OS': platform.system(),
            'OS_Version': platform.version(),
            'Machine': platform.machine(),
            'Processor': platform.processor(),
            'IP': socket.gethostbyname(socket.gethostname())
        }
        return system_info

    def get_ip_info(self):
        try:
            response = requests.get("https://get.geojs.io/v1/ip/geo.json")
            return response.json()
        except requests.RequestException:
            return {"country": "Unknown", "city": "Unknown", "ip": "Unknown"}

    def update(self, dt):
        ret, frame = self.capture.read()
        if not ret:
            self.info_label.text = "Unable to access the camera!"
            return

        results_hands = self.hands.process(frame)
        if results_hands.multi_hand_landmarks:
            for hand_landmarks in results_hands.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        emotions = []
        for (x, y, w, h) in faces:
            face = frame[y:y + h, x:x + w]
            try:
                result = DeepFace.analyze(face, actions=['emotion'], enforce_detection=False)
                emotion = result[0]['dominant_emotion']
                emotions.append(emotion)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            except Exception as e:
                print("Emotion detection error:", e)

        current_time = datetime.now().strftime("%H:%M:%S")

        hand_count = len(results_hands.multi_hand_landmarks) if results_hands.multi_hand_landmarks else 0
        face_count = len(faces)
        emotion_text = ", ".join(emotions) if emotions else "None"
        
        self.info_label.text = f"Faces: {face_count}, Hands: {hand_count}\n" \
                               f"Emotions: {emotion_text}\n" \
                               f"IP: {self.location_info.get('ip', 'Unknown')}\n" \
                               f"Location: {self.location_info.get('city', 'Unknown')}, {self.location_info.get('country', 'Unknown')}\n" \
                               f"OS: {self.system_info['OS']} {self.system_info['OS_Version']}\n" \
                               f"Time: {current_time}\n\n\n\n"

        buffer = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture

    def on_stop(self):
        self.capture.release()

if __name__ == "__main__":
    FaceHandEmotionApp().run()