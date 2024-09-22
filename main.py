import tkinter as tk

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Region Selector")

        self.canvas = tk.Canvas(root, bg="white", width=600, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.rect = None
        self.start_x = None
        self.start_y = None

        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        # Save the starting position
        self.start_x = event.x
        self.start_y = event.y

        # Create a rectangle
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="blue", width=2)

    def on_mouse_drag(self, event):
        # Update the rectangle's coordinates
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        # Get the coordinates of the selected region
        print(f"Selected region: ({self.start_x}, {self.start_y}) to ({event.x}, {event.y})")
        
        # Clear the rectangle after selection
        self.canvas.delete(self.rect)

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
