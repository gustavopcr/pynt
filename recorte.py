import draw

xmin = 200
xmax = 400
ymin = 300
ymax = 600

def region_code(x, y):
    codigo = 0
    
    if x < xmin:
        codigo = codigo + 1
    if x > xmax:
        codigo = codigo + 2
    if y < ymin:
        codigo + 4
    if y > ymax:
        codigo = codigo + 8
    
    return codigo


def cohen_sutherland(canvas, x1, y1, x2, y2):
    aceite = False
    feito = False

    while not feito:
        c1 = region_code(x1, y1)
        c2 = region_code(x2, y2)
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

            if cfora | 1:
                xint = xmin
                yint = y1+(y2-y1)*(xmin-x1)/(x2-x1)
            elif cfora | 2:
                xint = xmax
                yint = y1+(y2-y1)*(xmax-x1)/(x2-x1)
            elif cfora | 4:
                yint = ymin
                xint = x1+(x2-x1)*(ymin-y1)/(y2-y1)
            elif cfora | 8:
                yint = ymax
                xint = x1 +(x2-x1)*(ymax-y1)/(y2-y1)
            
            if c1 == cfora:
                x1=xint
                y1=yint
            else:
                x2=xint
                y2=yint
        if aceite:
            draw.dda(canvas, round(x1), round(y1), round(x2), round(y2))