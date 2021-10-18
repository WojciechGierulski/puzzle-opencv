import cv2 as cv

from cvzone.HandTrackingModule import HandDetector
from game import Game
from sets import Set
from geometry_funcs import GeometryFuncs

WIDTH = int(640 * 1.5)
HEIGHT = int(480 * 1.5)

cap = cv.VideoCapture(0, cv.CAP_DSHOW)
cap.set(cv.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, HEIGHT)
detector = HandDetector(detectionCon=0.75, maxHands=1)
set_nr = 1


def calibration():
    while True:
        success, img = cap.read()
        img = cv.flip(img, 1)
        original_img = img.copy()
        hand, img2 = detector.findHands(original_img)
        dist = GeometryFuncs.get_dist_between_fingers(hand)
        click = dist <= img2.shape[0] // 25
        if click:
            font = cv.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (0, 255, 0)
            thickness = 2
            org = (100, 100)
            img2 = cv.putText(img2, "Click detected, press space to continue", org, font,
                             fontScale, color, thickness, cv.LINE_AA)
        else:
            font = cv.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (0, 0, 255)
            thickness = 2
            org = (100, 100)
            img2 = cv.putText(img2, "Click not detected", org, font,
                             fontScale, color, thickness, cv.LINE_AA)
        cv.imshow("Calibration", img2)
        if cv.waitKey(1) == ord(" "):
            break


def start_game():
    global set_nr
    game1 = Game(set_nr, WIDTH, HEIGHT)

    while True:
        success, img = cap.read()
        img = cv.flip(img, 1)
        original_img = img.copy()
        hand, img2 = detector.findHands(original_img)

        img = game1.mainloop_iteration(img, hand)

        if not game1.win:
            cv.imshow("Puzzle", img)
            cv.waitKey(1)
        else:
            cv.imshow("Puzzle", img)
            if cv.waitKey(1) == ord(' '):
                set_nr += 1
                break


# Calibration
calibration()
cv.destroyAllWindows()
# Game
while set_nr != len(Set.SETS_SIZES.keys()) + 1:
    start_game()
cv.destroyAllWindows()
