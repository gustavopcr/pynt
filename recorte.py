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


    def clip_test(self, p, q, u1, u2):
        result = True
        if p < 0.0:
            r=q/p
            if r > u2:
                result = False
            elif r > u1:
                u1=r
        elif p>0.0:
            r = q/p
            if r<u1:
                result = False
            elif r < u2:
                u2 = r
        elif q<0.0:
            result = False
        return result
    
    def liang_barsky(self, x1, y1, x2, y2):
        u1 = 0.0
        u2 = 1.0
        dx = x2-x1
        dy = y2-y1

        if self.clip_test(self, -dx, x1 - self.xmin, u1, u2):
            if self.clip_test(dx, self.xmax - x1, u1, u2):
                if self.clip_test(-dy, y1 - self.ymin, u1, u2):
                    if self.clip_test(dy, self.ymax - y1, u1, u2):
                        if u2<1.0:
                            x2 = x1 +u2*dx
                            y2 = y1 +u2*dy
                        if u1>0.0:
                            x1=x1+u1*dx
                            y1=y1+u1*dy
                        draw.dda(round(x1), round(y1), round(x2), round(y2))