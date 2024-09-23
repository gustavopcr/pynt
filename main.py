import tkinter as tk

import draw

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.draw_mode = 0
        self.root.title("Paint App")
        self.canvas = tk.Canvas(root, bg="white", width=600, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.select_button = tk.Button(root, text="Select", command=self.activate_select)
        self.select_button.pack(side=tk.LEFT)

        self.line_button = tk.Button(root, text="Draw DDA", command=lambda: self.activate_draw(0))
        self.line_button.pack(side=tk.LEFT)

        self.line_button = tk.Button(root, text="Draw Bres", command=lambda: self.activate_draw(1))
        self.line_button.pack(side=tk.LEFT)

        self.line_button = tk.Button(root, text="Draw Circ", command=lambda: self.activate_draw(2))
        self.line_button.pack(side=tk.LEFT)

        self.rect = None
        self.line = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.mode = None  # 'select' or 'line'
        self.line_click_count = 0  # Track the number of clicks for drawing the line

        self.canvas.bind("<Button-1>", self.on_button_press)

    def activate_select(self):
        self.mode = 'select'

    def activate_draw(self, draw_mode):
        self.mode = 'line'
        self.draw_mode = draw_mode
        self.line_click_count = 0  # Reset click count when activating line mode

    def on_button_press(self, event):
        if self.mode == 'line':
            if self.line_click_count == 0:
                # First click, store the start point
                self.start_x = event.x
                self.start_y = event.y
                self.line_click_count = 1
            elif self.line_click_count == 1:
                # Second click, store the end point and draw the line
                self.end_x = event.x
                self.end_y = event.y
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
                self.line_click_count = 1  # Stay at 1 for the next line

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
