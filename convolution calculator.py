import tkinter as tk
from tkinter import ttk
import numpy as np
from scipy.signal import convolve2d
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from fractions import Fraction

class ConvolutionSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Convolution Simulator")
        self.root.geometry("1300x950")

        self.padding_var = tk.StringVar(value="zero")
        self.type_var = tk.StringVar(value="blur")
        self.alpha_var = tk.DoubleVar(value=0.4) # Based on your last scenario
        self.clip_var = tk.BooleanVar(value=False)
        self.range_var = tk.StringVar(value="0-1") # Matches your decimal input
        
        # Real-time trace for Section 1 ONLY
        for var in [self.padding_var, self.type_var, self.alpha_var, self.clip_var, self.range_var]:
            var.trace_add("write", lambda *args: self.generate_grids())

        self.input_entries = [] 
        self.kernel_entries = []
        
        self.setup_frame = ttk.LabelFrame(root, text="1. Configuration (Real-time)")
        self.setup_frame.pack(fill="x", padx=10, pady=5)
        
        self.matrix_input_frame = ttk.LabelFrame(root, text="2. Input Matrices (Manual)")
        self.matrix_input_frame.pack(fill="x", padx=10, pady=5)

        self.display_frame = ttk.LabelFrame(root, text="3. Visualization")
        self.display_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.create_setup_ui()
        self.generate_grids()

    def create_setup_ui(self):
        row1 = ttk.Frame(self.setup_frame)
        row1.pack(fill="x", padx=5, pady=5)
        ttk.Label(row1, text="Padding:").pack(side="left", padx=5)
        ttk.Combobox(row1, textvariable=self.padding_var, values=["zero", "replicate"], width=10, state="readonly").pack(side="left")
        ttk.Label(row1, text="Operation:").pack(side="left", padx=5)
        ttk.Combobox(row1, textvariable=self.type_var, values=["blur", "sharpen"], width=10, state="readonly").pack(side="left")
        ttk.Label(row1, text="Alpha:").pack(side="left", padx=5)
        ttk.Entry(row1, textvariable=self.alpha_var, width=5).pack(side="left")
        ttk.Label(row1, text="Range:").pack(side="left", padx=10)
        ttk.Radiobutton(row1, text="[0, 255]", variable=self.range_var, value="0-255").pack(side="left")
        ttk.Radiobutton(row1, text="[0.0, 1.0]", variable=self.range_var, value="0-1").pack(side="left")
        ttk.Checkbutton(row1, text="Clip", variable=self.clip_var).pack(side="left", padx=10)

        row2 = ttk.Frame(self.setup_frame)
        row2.pack(fill="x", padx=5, pady=5)
        ttk.Label(row2, text="Img Size:").pack(side="left")
        self.img_r = ttk.Entry(row2, width=3); self.img_r.insert(0, "4"); self.img_r.pack(side="left")
        self.img_c = ttk.Entry(row2, width=3); self.img_c.insert(0, "4"); self.img_c.pack(side="left")
        ttk.Label(row2, text="  Ker Size:").pack(side="left")
        self.ker_r = ttk.Entry(row2, width=3); self.ker_r.insert(0, "3"); self.ker_r.pack(side="left")
        self.ker_c = ttk.Entry(row2, width=3); self.ker_c.insert(0, "3"); self.ker_c.pack(side="left")
        for e in [self.img_r, self.img_c, self.ker_r, self.ker_c]: e.bind("<KeyRelease>", lambda e: self.generate_grids())

    def generate_grids(self):
        try:
            ir, ic = int(self.img_r.get()), int(self.img_c.get())
            kr, kc = int(self.ker_r.get()), int(self.ker_c.get())
        except: return

        self.update_matrix_ui("Input Image", self.input_entries, ir, ic)
        k_title = "Input Kernel" if self.type_var.get() == "blur" else "Input Blur Kernel (B)"
        self.update_matrix_ui(k_title, self.kernel_entries, kr, kc)

        if not hasattr(self, 'run_btn'):
            self.run_btn = ttk.Button(self.matrix_input_frame, text="Run Convolution", command=self.run_convolution)
            self.run_btn.pack(side="bottom", pady=5)
        self.run_convolution()

    def update_matrix_ui(self, title, entries_list, rows, cols):
        f_name = "Img" if "Image" in title else "Ker"
        target = next((w for w in self.matrix_input_frame.winfo_children() if getattr(w, 'id', '') == f_name), None)
        
        if not target:
            target = ttk.Frame(self.matrix_input_frame); target.id = f_name; target.pack(side="left", padx=10)
            target.lbl = ttk.Label(target, text=title, font=('Arial', 9, 'bold')); target.lbl.pack()
            target.grid = ttk.Frame(target); target.grid.pack()
        else: target.lbl.config(text=title)
        
        while len(entries_list) > rows: [e.destroy() for e in entries_list.pop()]
        for r in range(rows):
            if r >= len(entries_list): entries_list.append([])
            while len(entries_list[r]) > cols: entries_list[r].pop().destroy()
            while len(entries_list[r]) < cols:
                e = ttk.Entry(target.grid, width=6, justify="center")
                e.grid(row=r, column=len(entries_list[r]), padx=1, pady=1)
                entries_list[r].append(e)

    def get_val(self, entry):
        v = entry.get().strip()
        try: return float(Fraction(v)) if "/" in v else float(v) if v else 0.0
        except: return 0.0

    def format_smart(self, val):
        if float(val).is_integer(): return str(int(val))
        if round(val, 4) == round(val, 8): return str(round(val, 4)) # Terminating check
        f = Fraction(val).limit_denominator(1000)
        return f"{f.numerator}/{f.denominator}"

    def run_convolution(self):
        try:
            img = np.array([[self.get_val(e) for e in row] for row in self.input_entries])
            b_ker = np.array([[self.get_val(e) for e in row] for row in self.kernel_entries])
            
            if self.type_var.get() == "sharpen":
                alpha = self.alpha_var.get()
                kr, kc = b_ker.shape
                ident = np.zeros((kr, kc)); ident[kr//2, kc//2] = 1.0
                ker = (1 + alpha) * ident - (alpha * b_ker)
            else: ker = b_ker

            mode = 'fill' if self.padding_var.get() == 'zero' else 'symm'
            out = convolve2d(img, ker, mode='same', boundary=mode)
            if self.clip_var.get():
                limit = 255.0 if self.range_var.get() == "0-255" else 1.0
                out = np.clip(out, 0.0, limit)
            self.visualize(img, ker, out)
        except: pass

    def visualize(self, img, ker, out):
        for w in self.display_frame.winfo_children(): w.destroy()
        fig, axs = plt.subplots(1, 3, figsize=(12, 4))
        ph, pw = ker.shape[0]//2, ker.shape[1]//2
        pad = np.pad(img, ((ph, ph), (pw, pw)), mode='constant' if self.padding_var.get()=='zero' else 'edge')
        
        titles = ["Input (Padded)", "Actual Kernel used", "Output"]
        for i, (data, title) in enumerate(zip([pad, ker, out], titles)):
            axs[i].imshow(data, cmap='gray', vmin=0, vmax=255 if self.range_var.get()=="0-255" else 1.0 if i!=1 else None)
            axs[i].set_title(title, fontsize=9)
            for r in range(data.shape[0]):
                for c in range(data.shape[1]):
                    txt = self.format_smart(data[r, c])
                    color = "cyan" if (i==0 and (r<ph or r>=data.shape[0]-ph or c<pw or c>=data.shape[1]-pw)) else "red"
                    axs[i].text(c, r, txt, ha="center", va="center", color=color, fontsize=7, fontweight='bold')
            axs[i].axis('off')
        
        canvas = FigureCanvasTkAgg(fig, master=self.display_frame)
        canvas.draw(); canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

if __name__ == "__main__":
    root = tk.Tk(); app = ConvolutionSimulator(root); root.mainloop()