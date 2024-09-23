import draw
import math
class Transformacao:

    def __init__(self, xmin, xmax, ymin, ymax):
        # Initialize with boundaries for the clipping window
        self.points = [] #lista contendo todos os pontos apos transformacoes
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax


    # Transformação de translação
    def translate(self, p, dx, dy):
        x1, y1, x2, y2 = p
        new_x1, new_y1 = x1 + dx, y1 + dy
        new_x2, new_y2 = x2 + dx, y2 + dy
        return (new_x1, new_y1, new_x2, new_y2)

    # Transformação de rotação
    def rotate(self, p, angle_degrees):
        angle_radians = math.radians(angle_degrees)
        x1, y1, x2, y2 = p
        new_x1 = x1 * math.cos(angle_radians) - y1 * math.sin(angle_radians)
        new_y1 = x1 * math.sin(angle_radians) + y1 * math.cos(angle_radians)
        new_x2 = x2 * math.cos(angle_radians) - y2 * math.sin(angle_radians)
        new_y2 = x2 * math.sin(angle_radians) + y2 * math.cos(angle_radians)
        return (new_x1, new_y1, new_x2, new_y2)
    
    # Transformação de escala
    def scale(self, p, sx, sy):
        x1, y1, x2, y2 = p
        new_x1, new_y1 = x1 * sx, y1 * sy
        new_x2, new_y2 = x2 * sx, y2 * sy
        return (new_x1, new_y1, new_x2, new_y2)


    # Reflexão nos eixos X, Y ou XY
    def reflect_x(self, p):
        x1, y1, x2, y2 = p
        new_y1 = -y1
        new_y2 = -y2
        return (x1, new_y1, x2, new_y2)

    def reflect_y(self, p):
        x1, y1, x2, y2 = p
        new_x1 = -x1
        new_x2 = -x2
        return (new_x1, y1, new_x2, y2)

    def reflect_xy(self, p):
        x1, y1, x2, y2 = p
        new_x1, new_y1 = -x1, -y1
        new_x2, new_y2 = -x2, -y2
        return (new_x1, new_y1, new_x2, new_y2)

