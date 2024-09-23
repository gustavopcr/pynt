def draw_point(canvas, x, y, color="black"):
    canvas.create_oval(x-1, y-1, x+1, y+1, fill=color, outline=color)  # Drawing small points to represent the line
    

def plot_circle_points(canvas, xc, yc, x, y):
    draw_point(canvas, xc+x, yc+y)
    draw_point(canvas, xc-x, yc+y)
    draw_point(canvas, xc+x, yc-y)
    draw_point(canvas, xc-x, yc-y)
    draw_point(canvas, xc+y, yc+x)
    draw_point(canvas, xc-y, yc+x)
    draw_point(canvas, xc+y, yc-x)
    draw_point(canvas, xc-y, yc-x)

def dda(canvas, x1, y1, x2, y2):
    dx = dy = passos = 0
    x_incr = y_incr = x = y = 0.0

    dx = x2-x1
    dy = y2-y1
    if abs(dx)>abs(dy):
        passos = abs(dx)
    else:
        passos = abs(dy)
    
    x_incr = float(dx) / passos
    y_incr = float(dy) / passos

    x = x1
    y = y1
    draw_point(canvas, round(x), round(y))
    for k in range(passos + 1):
        x = x + x_incr
        y = y + y_incr
        draw_point(canvas, round(x), round(y))

def bresenham(canvas, x1, y1, x2, y2):
    dx = x2-x1
    dy = y2-y1
    if dx >= 0:
        incr_x = 1
    else:
        incr_x = -1
        dx = -dx
    
    if dy >= 0:
        incr_y = 1
    else:
        incr_y = -1
        dy = -dy

    x = x1
    y = y1
    draw_point(canvas, x, y)
    if dy<dx:
        p = 2*dy - dx
        const1=2*dy
        const2=2*(dy-dx)

        for i in range(dx):
            x += incr_x
            if p<0:
                p += const1
            else:
                y += incr_y
                p += const2
            draw_point(canvas, x, y)
    else:
        p = 2*dx-dy
        const1 = 2*dx
        const2 = 2*(dx-dy)
        for i in range(dy):
            y += incr_y
            if p<0:
                p += const1
            else:
                x += incr_x
                p += const2
            draw_point(canvas, x, y)

def circ_bresenhams(canvas, xc, yc, r):
    x = 0
    y = r
    p = 3-2*r
    plot_circle_points(canvas, xc, yc, x, y)
    while x<y:
        if p<0:
            p = p+4*x+6
        else:
            p = p+4*(4-y)+10
            y = y-1
        x=x+1
        plot_circle_points(canvas, xc, yc, x, y)


