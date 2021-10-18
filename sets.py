import os
import sys
import cv2 as cv
from puzzle import Puzzle
from random import randint


class Set:
    SETS_SIZES = {1: (2, 3), 2: (2, 4)}

    def __init__(self, set_nr, frame_size):
        self.set_nr = set_nr
        if os.path.isdir(f"sets/set{set_nr}"):
            self.size = self.SETS_SIZES[set_nr]
            self.images = {}
            row = 1
            col = 1
            for file_name in os.listdir(f"sets/set{set_nr}"):
                r_c = (row, col)
                self.images[r_c] = self.resize_img(cv.imread(f"sets/set{set_nr}/{row}{col}.jpg"), frame_size)
                if col == self.size[1]:
                    col = 1
                    row += 1
                else:
                    col += 1
        else:
            print("No such set")
            sys.exit(0)


    def resize_img(self, img, frame_size):
        scale = 0.15
        width = int(frame_size[0] * scale)
        height = int((width/img.shape[1]) * img.shape[0])
        return cv.resize(img, (height, width), interpolation=cv.INTER_AREA)


    def create_puzzles(self, frame_size):
        puzzles = []
        img_size = self.images[(1, 1)].shape
        for cords, img in self.images.items():
            x = randint(1, frame_size[0] - img_size[1] - 1)
            y = randint(int(0.05*frame_size[1]) + self.size[0] * img_size[0], frame_size[1] - img_size[0] - 1)
            height = img.shape[0]
            width = img.shape[1]
            puzzles.append(Puzzle(x, y, width, height, cords, self))
        return puzzles

