import tkinter as tk

import draw
from recorte import Recorte
from transformacao import Transformacao
class PaintApp:
    def __init__(self, root):
        self.points = [] #lista contendo todos os pontos
        self.root = root
        self.draw_mode = 0
        self.select_area = (0, 0, 0, 0) # x1, y1, x2, y2
        self.root.title("Paint App")
        self.canvas = tk.Canvas(root, bg="white", width=600, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.configs = Transformacao(0, 0, 0, 0, 0, 0)

        # Botão para abrir a janela de configuração
        self.config_button = tk.Button(root, text="Configurar Transformações", command=self.create_config_window)
        self.config_button.pack(pady=20)

        self.select_button = tk.Button(root, text="Select", command=self.activate_select)
        self.select_button.pack(side=tk.LEFT)
        
        self.translacao_button = tk.Button(root, text="Translação", command=lambda: self.activate_transformacao(0))
        self.translacao_button.pack(side=tk.LEFT)

        self.rotacao_button = tk.Button(root, text="Rotação", command=lambda: self.activate_transformacao(1))
        self.rotacao_button.pack(side=tk.LEFT)


        self.escala_button = tk.Button(root, text="Escala", command=lambda: self.activate_transformacao(2))
        self.escala_button.pack(side=tk.LEFT)

        self.reflexao_button = tk.Button(root, text="Reflexão", command=lambda: self.activate_transformacao(3))
        self.reflexao_button.pack(side=tk.LEFT)

        self.dda_button = tk.Button(root, text="DDA", command=lambda: self.activate_draw(0))
        self.dda_button.pack(side=tk.LEFT)

        self.bres_button = tk.Button(root, text="Bresenham", command=lambda: self.activate_draw(1))
        self.bres_button.pack(side=tk.LEFT)

        self.circ_bres_button = tk.Button(root, text="Circulo Bresenham", command=lambda: self.activate_draw(2))
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
            foo = rec.cohen_sutherland
        else:
            foo = rec.liang_barsky
        for p in self.points:
            foo(self.canvas, p[0], p[1], p[2], p[3])
        self.points = rec.points #atualiza pontos para refletir no recorte
        rec.points = [] #reseta lista de pontos do recorte para futuras iteracoes

    def activate_transformacao(self, transformacao_mode=0):
        t = Transformacao(self.configs.dx, self.configs.dy, self.configs.angle_degrees, self.configs.sx, self.configs.sy, self.configs.reflect_tipo)
        if transformacao_mode == 0: # translacao
            for i in range(len(self.points)):
                self.points[i] = t.translate(self.points[i], t.dx, t.dy) #10 e 10 -> dx e dy
        elif transformacao_mode == 1: # translacao
            for i in range(len(self.points)):
                self.points[i] = t.rotate(self.points[i], t.angle_degrees) #30 -> angulo
        elif transformacao_mode == 2: # translacao  
            for i in range(len(self.points)):
                self.points[i] = t.scale(self.points[i], t.sx, t.sy)
        else:
            if t.reflect_tipo == 0:
                for i in range(len(self.points)):
                    self.points[i] = t.reflect_x(self.canvas, self.points[i])
            elif t.reflect_tipo == 1:
                for i in range(len(self.points)):
                    self.points[i] = t.reflect_y(self.canvas, self.points[i])
            else:
                for i in range(len(self.points)):
                    self.points[i] = t.reflect_xy(self.canvas, self.points[i])
        self.canvas.delete("all")
        for p in self.points:
            draw.dda(self.canvas, p[0], p[1], p[2], p[3])


        #redraw
    def on_button_press(self, event):
        if self.mode == 'select':
            self.start_x = event.x
            self.start_y = event.y
            if self.rect:
                self.canvas.delete(self.rect) #se rect ja existe, apaga
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="blue", width=2)
        elif self.mode == 'line':
            if self.line_click_count == 0:
                self.start_x = event.x
                self.start_y = event.y
                self.line_click_count = 1
            elif self.line_click_count == 1:
                self.end_x = event.x
                self.end_y = event.y
                self.points.append( (self.start_x, self.start_y, self.end_x, self.end_y) )
                if self.draw_mode == 0:
                    draw.dda(self.canvas, self.start_x, self.start_y, self.end_x, self.end_y)
                elif self.draw_mode == 1:
                    draw.bresenham(self.canvas, self.start_x, self.start_y, self.end_x, self.end_y)
                elif self.draw_mode == 2:
                    draw.circ_bresenhams(self.canvas, self.end_x, self.end_y, 10)
                self.start_x = self.end_x
                self.start_y = self.end_y
                self.line_click_count = 0 # reseta contagem de pontos


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

    def create_config_window(self):
        self.config_window = tk.Toplevel(self.root)
        self.config_window.title("Configurações")

        # Translação
        tk.Label(self.config_window, text="Translação:").grid(row=0, columnspan=2, pady=5)
        self.dx_entry = tk.Entry(self.config_window)
        self.dx_entry.grid(row=1, column=0)
        tk.Label(self.config_window, text="dx").grid(row=1, column=1)

        self.dy_entry = tk.Entry(self.config_window)
        self.dy_entry.grid(row=2, column=0)
        tk.Label(self.config_window, text="dy").grid(row=2, column=1)

        # Rotação
        tk.Label(self.config_window, text="Rotação:").grid(row=3, columnspan=2, pady=5)
        self.angle_entry = tk.Entry(self.config_window)
        self.angle_entry.grid(row=4, column=0)
        tk.Label(self.config_window, text="Ângulo (graus)").grid(row=4, column=1)

        # Escala
        tk.Label(self.config_window, text="Escala:").grid(row=5, columnspan=2, pady=5)
        self.sx_entry = tk.Entry(self.config_window)
        self.sx_entry.grid(row=6, column=0)
        tk.Label(self.config_window, text="sx").grid(row=6, column=1)

        self.sy_entry = tk.Entry(self.config_window)
        self.sy_entry.grid(row=7, column=0)
        tk.Label(self.config_window, text="sy").grid(row=7, column=1)

        # Reflexão
        tk.Label(self.config_window, text="Reflexão:").grid(row=8, columnspan=2, pady=5)

        self.reflect_var = tk.IntVar()
        tk.Radiobutton(self.config_window, text="Refletir em X", variable=self.reflect_var, value=0).grid(row=9, columnspan=2)
        tk.Radiobutton(self.config_window, text="Refletir em Y", variable=self.reflect_var, value=1).grid(row=10, columnspan=2)
        tk.Radiobutton(self.config_window, text="Refletir em XY", variable=self.reflect_var, value=2).grid(row=11, columnspan=2)

        # Botão para aplicar transformações
        tk.Button(self.config_window, text="Aplicar", command=self.save_config).grid(row=12, columnspan=2, pady=10)


    def save_config(self):
        # Atualiza a instância de TransformConfig com os valores das entradas
        try:
            dx = float(self.dx_entry.get())
            dy = float(self.dy_entry.get())
            angle = float(self.angle_entry.get())
            sx = float(self.sx_entry.get())
            sy = float(self.sy_entry.get())
            reflection_type = self.reflect_var.get()

            # Atualiza o objeto transform_config
            self.configs = Transformacao(dx, dy, angle, sx, sy, reflection_type)
            # Aqui você pode retornar o objeto de configuração se desejar
            print("Configurações salvas:", self.configs)
            self.config_window.destroy()  # Fechar a janela de configurações
        except ValueError:
            print("Por favor, insira valores válidos.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
