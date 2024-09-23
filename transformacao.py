import draw

class Transformacao:

    def __init__(self, xmin, xmax, ymin, ymax):
        # Initialize with boundaries for the clipping window
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax