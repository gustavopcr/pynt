import tkinter as tk

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint App")

        self.canvas = tk.Canvas(root, bg="white", width=600, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.select_button = tk.Button(root, text="Select", command=self.activate_select)
        self.select_button.pack(side=tk.LEFT)

        self.line_button = tk.Button(root, text="Draw Line", command=self.activate_line)
        self.line_button.pack(side=tk.LEFT)

        self.rect = None
        self.line = None
        self.start_x = None
        self.start_y = None
        self.mode = None  # 'select' or 'line'

        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def activate_select(self):
        self.mode = 'select'

    def activate_line(self):
        self.mode = 'line'

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

        if self.mode == 'select':
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="blue", width=2)
        elif self.mode == 'line':
            self.line = self.canvas.create_line(self.start_x, self.start_y, self.start_x, self.start_y, fill="red", width=2)

    def on_mouse_drag(self, event):
        if self.mode == 'select' and self.rect:
            self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)
        elif self.mode == 'line' and self.line:
            self.canvas.coords(self.line, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        if self.mode == 'select':
            print(f"Selected region: ({self.start_x}, {self.start_y}) to ({event.x}, {event.y})")
            self.canvas.delete(self.rect)
        elif self.mode == 'line':
            print(f"Drew line from: ({self.start_x}, {self.start_y}) to ({event.x}, {event.y})")

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
