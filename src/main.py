import tkinter as tk
from src.gui.clock_canvas import AnalogClock

class ClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Reloj Analógico Python')
        dark_bg = '#1f1f1f'
        self.root.configure(bg=dark_bg)
        self.frame = tk.Frame(root, bg=dark_bg)
        self.frame.pack(expand=True, fill='both', padx=10, pady=10)

        self.clock = AnalogClock(self.frame)

def main():
    root = tk.Tk()
    app = ClockApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()