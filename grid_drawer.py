import cv2 as cv


class GridDrawer:

    def __init__(self, frame_size, puzzle_size, set_size):
        self.frame_size = frame_size
        self.puzzle_size = puzzle_size
        self.set_size = set_size  # rows, cols
        self.grid_x = []
        self.grid_y = []
        self.calculate_grid_sizes()

    def calculate_grid_sizes(self):
        x_free_space = (self.frame_size[0] - (self.set_size[1] * self.puzzle_size[0])) // 2
        self.grid_x.append(x_free_space)
        y_free_space = int(self.frame_size[1] * 0.05)
        self.grid_y.append(y_free_space)
        for i in range(self.set_size[1]):
            self.grid_x.append((i+1) * self.puzzle_size[0] + x_free_space)
        for i in range(self.set_size[0]):
            self.grid_y.append((i+1) * self.puzzle_size[1] + y_free_space)

    def draw_grid(self, img, good_puzzles, level_passed):
        if not level_passed:
            for x_point in self.grid_x:
                cv.line(img, (x_point, self.grid_y[0]), (x_point, self.grid_y[-1]), (0, 0, 0), thickness=1)
            for y_point in self.grid_y:
                cv.line(img, (self.grid_x[0], y_point), (self.grid_x[-1], y_point), (0, 0, 0), thickness=1)

            for puzzle in good_puzzles:
                cv.rectangle(img, (puzzle.x, puzzle.y), (puzzle.x+puzzle.width, puzzle.y+puzzle.height), (0, 255, 0), 2)


