import cv2 as cv

from geometry_funcs import GeometryFuncs
from grid_drawer import GridDrawer
from sets import Set


class Game:
    def __init__(self, set_nr, width, height):
        self.set = Set(set_nr, (width, height))
        self.puzzles = self.set.create_puzzles((width, height))
        self.puzzle_size = (self.puzzles[0].width, self.puzzles[0].height)
        self.frame_size = (width, height)
        self.dragged_puzzle = None
        self.grid_drawer = GridDrawer(self.frame_size, self.puzzle_size, Set.SETS_SIZES[set_nr])
        self.good_puzzles = []
        self.win = False

    def draw_puzzles(self, img):
        for puzzle in self.puzzles:
            img = puzzle.draw_on_img(img)
        return img

    def check_if_puzzle_clicked(self, hand, puzzle, img_shape):
        if hand:
            click_distance = img_shape[0] // 25
            if GeometryFuncs.get_dist_between_fingers(hand) < click_distance:
                mean_point = GeometryFuncs.mean_point(hand)
                if GeometryFuncs.point_in_rect(mean_point, puzzle):
                    grab_point = [mean_point[0] - puzzle.x, mean_point[1] - puzzle.y]
                    return grab_point
            return False
        return False

    def check_unclick(self, hand, img):
        unclick_distance = img.shape[0] // 20
        if GeometryFuncs.get_dist_between_fingers(hand) > unclick_distance:
            puzzle = self.dragged_puzzle
            puzzle.grabbed = False
            puzzle.grab_point = None
            if self.check_if_puzzle_dropped_correctly(puzzle):
                puzzle.good = True
                self.good_puzzles.append(puzzle)
                puzzle.x = self.grid_drawer.grid_x[puzzle.cords[1] - 1]
                puzzle.y = self.grid_drawer.grid_y[puzzle.cords[0] - 1]
            self.dragged_puzzle = None

    def drag_puzzles(self, hand):
        puzzle = self.dragged_puzzle
        puzzle.prv_x = puzzle.x
        puzzle.prv_y = puzzle.y
        mean_point = GeometryFuncs.mean_point(hand)
        puzzle.x = mean_point[0] - puzzle.grab_point[0]
        puzzle.y = mean_point[1] - puzzle.grab_point[1]

    def check_clicks(self, hand, img):
        for puzzle in self.puzzles:
            if not puzzle.good:
                if grab_point := self.check_if_puzzle_clicked(hand, puzzle, img.shape):
                    if not puzzle.grabbed:
                        puzzle.grabbed = True
                        puzzle.grab_point = grab_point
                        self.dragged_puzzle = puzzle
                        break

    def check_if_puzzle_dropped_correctly(self, puzzle):
        puzzle_space = (self.grid_drawer.grid_x[puzzle.cords[1] - 1], self.grid_drawer.grid_y[puzzle.cords[0] - 1])
        area_percentage = GeometryFuncs.intersect_area(puzzle, puzzle_space)
        return area_percentage >= 0.9

    def draw_text(self, img):
        font = cv.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        color = (255, 0, 0)
        thickness = 2
        if self.set.set_nr == len(Set.SETS_SIZES.keys()):
            text = "Press space to finish the game"
        else:
            text = "Press space to go to the next level"
        s, b = cv.getTextSize(text, font, fontScale, thickness)
        org = (self.frame_size[0] // 2 - s[0] // 2, self.frame_size[1] // 2 - s[1] // 2)
        img = cv.putText(img, text, org, font,
                         fontScale, color, thickness, cv.LINE_AA)
        return img

    def mainloop_iteration(self, img, hand):
        if not self.dragged_puzzle:
            self.check_clicks(hand, img)
        if self.dragged_puzzle:
            self.check_unclick(hand, img)
        if self.dragged_puzzle:
            self.drag_puzzles(hand)
        img = self.draw_puzzles(img)
        self.grid_drawer.draw_grid(img, self.good_puzzles, self.win)

        # Check win condition
        if len(self.good_puzzles) == self.set.size[0] * self.set.size[1]:
            self.win = True
            img = self.draw_text(img)
        return img
