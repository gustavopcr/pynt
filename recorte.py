import draw

class Recorte:

    def __init__(self, xmin, xmax, ymin, ymax):
        # Initialize with boundaries for the clipping window
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

    def region_code(self, x, y):
        codigo = 0
        
        if x < self.xmin:
            codigo = codigo + 1
        if x > self.xmax:
            codigo = codigo + 2
        if y < self.ymin:
            codigo = codigo + 4
        if y > self.ymax:
            codigo = codigo + 8
        
        return codigo


    def cohen_sutherland(self, canvas, x1, y1, x2, y2):
        aceite = False
        feito = False

        while not feito:
            c1 = self.region_code(x1, y1)
            c2 = self.region_code(x2, y2)
            if c1 == 0 and c2 == 0:
                aceite = True
                feito = True
            elif c1 != 0 and c2 !=0:
                feito = True
            else:
                if c1 != 0:
                    cfora = c1
                else:
                    cfora = c2

                if cfora & 1:
                    xint = self.xmin
                    yint = y1+(y2-y1)*(self.xmin-x1)/(x2-x1)
                elif cfora & 2:
                    xint = self.xmax
                    yint = y1+(y2-y1)*(self.xmax-x1)/(x2-x1)
                elif cfora & 4:
                    yint = self.ymin
                    xint = x1+(x2-x1)*(self.ymin-y1)/(y2-y1)
                elif cfora & 8:
                    yint = self.ymax
                    xint = x1 +(x2-x1)*(self.ymax-y1)/(y2-y1)
                
                if c1 == cfora:
                    x1=xint
                    y1=yint
                else:
                    x2=xint
                    y2=yint
            if aceite:
                draw.dda(canvas, round(x1), round(y1), round(x2), round(y2))