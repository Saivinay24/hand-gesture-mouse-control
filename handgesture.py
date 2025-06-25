import cv2
import mediapipe as mp
import pyautogui
import webbrowser


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()
def hand_landmark_to_screen(landmark, frame_width, frame_height):
    x = int(landmark.x * frame_width)
    y = int(landmark.y * frame_height)
    screen_x = int((x / frame_width) * screen_width)
    screen_y = int((y / frame_height) * screen_height)
    return screen_x, screen_y

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_height, frame_width, _ = frame.shape


    result = hands.process(frame_rgb)


    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)


            index_finger_tip = hand_landmarks.landmark[8]
            screen_x, screen_y = hand_landmark_to_screen(index_finger_tip, frame_width, frame_height)
            pyautogui.moveTo(screen_x, screen_y)
            thumb_tip = hand_landmarks.landmark[4]
            thumb_x, thumb_y = hand_landmark_to_screen(thumb_tip, frame_width, frame_height)
            distance = ((screen_x - thumb_x) ** 2 + (screen_y - thumb_y) ** 2) ** 0.5
            if distance <30 : #  webbrowser.open("https://www.youtube.com/s");
                pyautogui.click();
            cv2.imshow("Hand Gesture Mouse Control", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
             break
cap.release()
cv2.destroyAllWindows()
