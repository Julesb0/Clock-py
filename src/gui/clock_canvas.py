import tkinter as tk
import math
import time
from src.models.linked_list import CircularDoublyLinkedList

class AnalogClock:
    def __init__(self, root):
        self.root = root
        # Tema oscuro fijo
        self.current_theme = {
            'bg': '#222222',
            'face': '#2f2f2f',
            'numbers': '#e6e6e6',
            'hour_hand': '#ffffff',
            'min_hand': '#ffffff',
            'sec_hand': '#ff6b6b',
            'ticks': '#6f6f6f'
        }

        # Canvas y digital label (todo oscuro)
        self.canvas = tk.Canvas(root, width=420, height=420, bg=self.current_theme['bg'], highlightthickness=0)
        self.canvas.pack()
        self.digital = tk.Label(root, text='', bg=self.current_theme['bg'], fg=self.current_theme['numbers'], font=('Arial', 14))
        self.digital.pack(pady=(6,0))

        # Configuración del reloj
        self.center = (210, 210)
        self.R = 180

        # Estructura de datos
        self.ticks = CircularDoublyLinkedList.build_ticks(60)

        # Sincronizar con hora actual
        now = time.localtime()
        self._sync_nodes(now)

        # Dibujar esfera y arrancar
        self.draw_static()
        self.update_clock()

    def _sync_nodes(self, now):
        self.sec_node = self.ticks.get_node_at(now.tm_sec)
        self.min_node = self.ticks.get_node_at(now.tm_min)
        hour_pos = (now.tm_hour % 12) * 5 + (now.tm_min // 12)
        self.hour_node = self.ticks.get_node_at(hour_pos)

    def draw_static(self):
        cx, cy = self.center
        self.canvas.delete('static')
        # esfera
        self.canvas.create_oval(cx-self.R, cy-self.R, cx+self.R, cy+self.R,
                                fill=self.current_theme['face'],
                                outline=self.current_theme['ticks'],
                                width=3,
                                tags='static')
        # marcadores y números
        for i in range(60):
            angle = math.radians(i * 6 - 90)
            outer_r = self.R
            inner_r = self.R - (18 if i % 5 == 0 else 8)
            start = (cx + inner_r * math.cos(angle), cy + inner_r * math.sin(angle))
            end = (cx + outer_r * math.cos(angle), cy + outer_r * math.sin(angle))
            width = 3 if i % 5 == 0 else 1
            self.canvas.create_line(start[0], start[1], end[0], end[1],
                                    fill=self.current_theme['ticks'], width=width, tags='static')
            if i % 5 == 0:
                num = i // 5 if i > 0 else 12
                num_r = self.R - 45
                tx = cx + num_r * math.cos(angle)
                ty = cy + num_r * math.sin(angle)
                self.canvas.create_text(tx, ty, text=str(num),
                                        fill=self.current_theme['numbers'],
                                        font=('Arial', 14, 'bold'),
                                        tags='static')

    def draw_hand(self, angle_deg, length, width, color):
        cx, cy = self.center
        angle = math.radians(angle_deg - 90)
        x = cx + math.cos(angle) * length
        y = cy + math.sin(angle) * length
        return self.canvas.create_line(cx, cy, x, y, width=width, fill=color, capstyle='round', tags='hands')

    def update_clock(self):
        # Usar hora real para digital y sincronizar nodos (evita drift)
        now = time.localtime()
        self._sync_nodes(now)

        # Texto digital HH:MM:SS AM/PM
        hh = now.tm_hour
        ampm = 'AM' if hh < 12 else 'PM'
        disp_h = hh % 12
        disp_h = disp_h if disp_h != 0 else 12
        digital_text = f'{disp_h:02d}:{now.tm_min:02d}:{now.tm_sec:02d} {ampm}'
        self.digital.config(text=digital_text)

        # borrar manos anteriores
        self.canvas.delete('hands')

        # calcular ángulos a partir de nodos (preciso y consistente)
        sec_deg = self.sec_node.data['deg']
        min_deg = self.min_node.data['deg'] + (self.sec_node.data['index'] / 60) * 6
        hour_deg = self.hour_node.data['deg'] + (self.min_node.data['index'] / 60) * 30

        # dibujar manos
        self.draw_hand(hour_deg, self.R * 0.5, 6, self.current_theme['hour_hand'])
        self.draw_hand(min_deg, self.R * 0.72, 4, self.current_theme['min_hand'])
        self.draw_hand(sec_deg, self.R * 0.9, 2, self.current_theme['sec_hand'])

        # centro
        cx, cy = self.center
        self.canvas.create_oval(cx-6, cy-6, cx+6, cy+6, fill=self.current_theme['hour_hand'], tags='hands')

        # avanzar nodos (siguiente segundo)
        self.sec_node = self.sec_node.next
        if self.sec_node.data['index'] == 0:
            self.min_node = self.min_node.next
            if self.min_node.data['index'] == 0:
                self.hour_node = self.hour_node.next

        # programar siguiente actualización
        self.root.after(1000, self.update_clock)
