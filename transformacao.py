import draw
import math
class Transformacao:

    def __init__(self, dx, dy, angle_degrees, sx, sy, reflect_tipo):
        # Initialize with boundaries for the clipping window
        self.dx = dx
        self.dy = dy
        self.angle_degrees = angle_degrees
        self.sx = sx
        self.sy = sy
        self.reflect_tipo = reflect_tipo

    # Método para mover os pontos para a origem
    def move_to_origin(self, p):
        # Calcular o ponto médio da linha
        x1, y1, x2, y2 = p
        cx = (x1 + x2) / 2  # Cálculo do centro X
        cy = (y1 + y2) / 2  # Cálculo do centro Y
        
        # Transladar os pontos para a origem
        return self.translate(p, -cx, -cy), (cx, cy)  # Retornar o ponto de origem para reverter depois


    # Transformação de translação
    def translate(self, p, dx, dy):
        x1, y1, x2, y2 = p
        new_x1, new_y1 = x1 + dx, y1 + dy
        new_x2, new_y2 = x2 + dx, y2 + dy
        return (new_x1, new_y1, new_x2, new_y2)

    # Transformação de rotação
    def rotate(self, p, angle_degrees):
        # Mover para a origem
        p, (cx, cy) = self.move_to_origin(p)  
        x1, y1, x2, y2 = p
        # Aplicar a rotação
        angle_radians = math.radians(angle_degrees)
        new_x1 = x1 * math.cos(angle_radians) - y1 * math.sin(angle_radians)
        new_y1 = x1 * math.sin(angle_radians) + y1 * math.cos(angle_radians)
        new_x2 = x2 * math.cos(angle_radians) - y2 * math.sin(angle_radians)
        new_y2 = x2 * math.sin(angle_radians) + y2 * math.cos(angle_radians)

        # Transladar de volta
        return self.translate((new_x1, new_y1, new_x2, new_y2), cx, cy)
    
    # Transformação de escala
    def scale(self, p, sx, sy):
        # Mover para a origem
        p, (cx, cy) = self.move_to_origin(p)  
        x1, y1, x2, y2 = p
        
        # Aplicar a escala
        new_x1, new_y1 = x1 * sx, y1 * sy
        new_x2, new_y2 = x2 * sx, y2 * sy

        # Transladar os pontos de volta ao local original
        return self.translate((new_x1, new_y1, new_x2, new_y2), cx, cy)


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

