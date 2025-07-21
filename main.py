import cv2
import mediapipe as mp
import pyautogui
import speech_recognition as sr
import pyttsx3
import time
from datetime import datetime

# Voice setup
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

def speak(text):
    print("🗣️ Speaking:", text)
    engine.say(text)
    engine.runAndWait()

# Voice command function
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening for command...")
        audio = recognizer.listen(source)
        try:
            cmd = recognizer.recognize_google(audio)
            print("🗣️ You said:", cmd)
            return cmd.lower()
        except:
            print("❌ Could not understand.")
            return ""

# Camera and Hand Detection
cap = cv2.VideoCapture(0)
hands = mp.solutions.hands.Hands()
draw = mp.solutions.drawing_utils
screen_w, screen_h = pyautogui.size()

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            draw.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)

            index = hand.landmark[8]
            x = int(index.x * w)
            y = int(index.y * h)

            screen_x = screen_w * index.x
            screen_y = screen_h * index.y
            pyautogui.moveTo(screen_x, screen_y)

            thumb = hand.landmark[4]
            thumb_x = int(thumb.x * w)
            thumb_y = int(thumb.y * h)

            if abs(x - thumb_x) < 30 and abs(y - thumb_y) < 30:
                pyautogui.click()
                speak("Clicked")
                time.sleep(0.3)

    cv2.imshow("AI Virtual Mouse", frame)

    key = cv2.waitKey(1)
    if key == ord('v'):
        command = listen_command()

        if "click" in command:
            pyautogui.click()
            speak("Clicking")
        elif "double click" in command:
            pyautogui.doubleClick()
            speak("Double clicked")
        elif "right click" in command:
            pyautogui.rightClick()
            speak("Right click")
        elif "scroll down" in command:
            pyautogui.scroll(-500)
            speak("Scrolling down")
            
        elif "scroll up" in command:
            pyautogui.scroll(500)
            speak("Scrolling up")
        elif "open notepad" in command:
            pyautogui.hotkey('win', 'r')
            time.sleep(1)
            pyautogui.write("notepad")
            pyautogui.press('enter')
            speak("Opening Notepad")
        elif "open google chrome" in command:
            pyautogui.hotkey('win', 'r')
            time.sleep(1)
            pyautogui.write("chrome")
            pyautogui.press('enter')
            speak("Opening Google Chrome")
        elif "time" in command or "what is the time" in command:
            now = datetime.now().strftime("%I:%M %p")
            speak("The time is " + now)
        else:
            speak("Command not recognized")

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
