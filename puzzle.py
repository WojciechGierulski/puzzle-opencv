import cv2 as cv


class Puzzle:
    COLOR = (255, 0, 255)

    def __init__(self, x, y, width, height, cords, set, alpha=0.3):
        self.alpha = alpha
        self.x = x
        self.y = y
        self.prv_x = 0
        self.prv_y = 0
        self.width = width
        self.height = height
        self.cords = cords
        self.grabbed = False
        self.grab_point = None
        self.set = set
        self.good = False  # If puzzle is placed in good spot

    def draw_on_img(self, img):
        # draws on original image
        overlay = self.set.images[self.cords]
        o_height, o_width, _ = overlay.shape
        if self.good:
            self.alpha = 0.0
        if self.grabbed:
            cv.rectangle(img, (self.x, self.y), (self.x + self.width, self.y + self.height), (0, 0, 255), 5)
        try:
            fragment = cv.addWeighted(img[self.y:self.y + o_height, self.x:self.x + o_width], self.alpha, overlay,
                                      1 - self.alpha, 0)
            img[self.y:self.y + o_height, self.x:self.x + o_width] = fragment
            return img
        except:
            self.x = self.prv_x
            self.y = self.prv_y
            fragment = cv.addWeighted(img[self.y:self.y + o_height, self.x:self.x + o_width], self.alpha, overlay,
                                      1 - self.alpha, 0)
            img[self.y:self.y + o_height, self.x:self.x + o_width] = fragment
            return img
