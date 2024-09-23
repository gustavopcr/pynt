import tkinter as tk

import draw
from recorte import Recorte

class PaintApp:
    def __init__(self, root):
        self.points = [] #lista contendo todos os pontos
        self.root = root
        self.draw_mode = 0
        self.select_area = (0, 0, 0, 0) # x1, y1, x2, y2
        self.root.title("Paint App")
        self.canvas = tk.Canvas(root, bg="white", width=600, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.select_button = tk.Button(root, text="Select", command=self.activate_select)
        self.select_button.pack(side=tk.LEFT)

        self.dda_button = tk.Button(root, text="Draw DDA", command=lambda: self.activate_draw(0))
        self.dda_button.pack(side=tk.LEFT)

        self.bres_button = tk.Button(root, text="Draw Bres", command=lambda: self.activate_draw(1))
        self.bres_button.pack(side=tk.LEFT)

        self.circ_bres_button = tk.Button(root, text="Draw Circ", command=lambda: self.activate_draw(2))
        self.circ_bres_button.pack(side=tk.LEFT)

        self.cohen_button = tk.Button(root, text="Cohen-Sutherland", command=lambda: self.activate_recorte(0))
        self.cohen_button.pack(side=tk.LEFT)

        self.liang_button = tk.Button(root, text="Liang-Barsky", command=lambda: self.activate_recorte(1))
        self.liang_button.pack(side=tk.LEFT)



        self.rect = None
        self.line = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.mode = None  # 'select' or 'line'
        self.line_click_count = 0  # Track the number of clicks for drawing the line

                # Bind mouse events for selection
        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def activate_select(self):
        self.mode = 'select'

    def activate_draw(self, draw_mode):
        self.mode = 'line'
        self.draw_mode = draw_mode
        self.line_click_count = 0  # Reset click count when activating line mode

    def activate_recorte(self, recorte_mode=0):
        rec = Recorte(xmin=self.select_area[0], ymin=self.select_area[1], xmax=self.select_area[2], ymax=self.select_area[3])
        self.canvas.delete("all")
        if recorte_mode == 0:
            print("cohen_sutherland")
            foo = rec.cohen_sutherland
        else:
            print("liang_barsky")
            foo = rec.liang_barsky
        for p in self.points:
            #rec.cohen_sutherland(self.canvas, p[0], p[1], p[2], p[3])
            foo(self.canvas, p[0], p[1], p[2], p[3])
        self.points = rec.points
        rec.points = []
        
    def on_button_press(self, event):

        if self.mode == 'select':
            self.start_x = event.x
            self.start_y = event.y
            if self.rect:
                self.canvas.delete(self.rect)
            # Create a new rectangle that will be updated as the user drags
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="blue", width=2)
        elif self.mode == 'line':
            if self.line_click_count == 0:
                # First click, store the start point
                self.start_x = event.x
                self.start_y = event.y
                self.line_click_count = 1
            elif self.line_click_count == 1:
                # Second click, store the end point and draw the line
                self.end_x = event.x
                self.end_y = event.y
                self.points.append( (self.start_x, self.start_y, self.end_x, self.end_y) )
                if self.draw_mode == 0:
                    draw.dda(self.canvas, self.start_x, self.start_y, self.end_x, self.end_y)
                elif self.draw_mode == 1:
                    draw.dda(self.canvas, self.start_x, self.start_y, self.end_x, self.end_y)
                elif self.draw_mode == 2:
                    draw.circ_bresenhams(self.canvas, self.end_x, self.end_y, 10)
                    #draw.dda(self.canvas, self.start_x, self.start_y, self.end_x, self.end_y)
                #draw_dda_line(self.start_x, self.start_y, self.end_x, self.end_y)
                # After drawing the line, reset start point for the next line
                self.start_x = self.end_x
                self.start_y = self.end_y
                self.line_click_count = 0


    def on_mouse_drag(self, event):
        # Update the size of the rectangle as the mouse is dragged
        if self.mode == "select":
            cur_x, cur_y = (event.x, event.y)
            # Expand the rectangle as the user drags the mouse
            self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        # Final coordinates when the mouse button is released
        if self.mode == "select":    
            end_x, end_y = event.x, event.y
            # Log the coordinates of the selected area
            print(f"Selected area: ({self.start_x}, {self.start_y}) to ({end_x}, {end_y})")
            self.select_area = (self.start_x, self.start_y, end_x, end_y)

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
