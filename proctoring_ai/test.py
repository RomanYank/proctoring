import cv2
from GazeTracking.gaze_tracking import GazeTracking
import matplotlib.pyplot as plt

def main():
    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not webcam.isOpened():
        print("Cannot open webcam")
        return

    plt.ion()  # включаем интерактивный режим matplotlib
    fig, ax = plt.subplots()

    while True:
        ret, frame = webcam.read()
        if not ret:
            break

        gaze.refresh(frame)
        annotated_frame = gaze.annotated_frame()
        text = ""
        if gaze.is_right():
            text = "Looking right"
        elif gaze.is_left():
            text = "Looking left"
        elif gaze.is_center():
            text = "Looking center"

        cv2.putText(annotated_frame, text, (60, 60), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 2)

        # OpenCV использует BGR, matplotlib - RGB, конвертируем:
        annotated_frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)

        ax.imshow(annotated_frame_rgb)
        plt.axis('off')
        plt.pause(0.001)
        ax.clear()

        # Можно выйти по нажатию клавиши q в консоли
        import msvcrt
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'q':
                break

    webcam.release()
    plt.close()

if __name__ == "__main__":
    main()
