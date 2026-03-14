import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import numpy as np
import solvers  # Importing our logic module

class SLAESolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SLAE Solver Pro")
        self.root.geometry("850x650")
        self.root.configure(bg="#f5f5f7")

        self.entries_a = []
        self.entries_b = []

        style = ttk.Style()
        style.configure("TFrame", background="#f5f5f7")
        style.configure("TLabel", background="#f5f5f7", font=("Segoe UI", 10))

        # UI components setup (Header, Control Panel, Canvas, etc.)
        # [The same layout code as before, but calling solvers.func()]
        self._setup_ui()
        self.update_grid()

    def _setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#2c3e50", height=60)
        header.pack(fill=tk.X)
        tk.Label(header, text="SLAE Matrix Solver", bg="#2c3e50", fg="white",
                 font=("Segoe UI", 16, "bold")).pack(pady=10)

        # Control Panel
        ctrl_frame = ttk.Frame(self.root, padding=15)
        ctrl_frame.pack(fill=tk.X)

        ttk.Label(ctrl_frame, text="Dimension (n):").grid(row=0, column=0, padx=5)
        self.n_var = tk.IntVar(value=3)
        self.n_spin = ttk.Spinbox(ctrl_frame, from_=2, to=10, width=5,
                                  textvariable=self.n_var, command=self.update_grid)
        self.n_spin.grid(row=0, column=1, padx=5)

        ttk.Label(ctrl_frame, text="Method:").grid(row=0, column=2, padx=20)
        self.method_var = tk.StringVar(value="Gauss")
        self.method_cb = ttk.Combobox(ctrl_frame, textvariable=self.method_var,
                                      values=["Cramer", "Gauss", "Gauss-Jordan", "Jacobi", "Seidel"],
                                      state="readonly", width=15)
        self.method_cb.grid(row=0, column=3, padx=5)

        # Matrix Area
        self.main_container = ttk.Frame(self.root, padding=10)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.main_container, bg="white", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Result Area
        self.res_frame = tk.Frame(self.root, bg="#ecf0f1", height=100)
        self.res_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.lbl_result = tk.Label(self.res_frame, text="Enter data and click 'Solve'",
                                   bg="#ecf0f1", font=("Consolas", 11), justify=tk.LEFT)
        self.lbl_result.pack(pady=15)

        # Buttons
        btn_frame = ttk.Frame(self.root, padding=10)
        btn_frame.pack(side=tk.BOTTOM)
        ttk.Button(btn_frame, text="📁 Load File", command=self.load_file).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="🔄 Clear", command=self.clear_fields).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Solve ✨", command=self.solve, bg="#27ae60", fg="white",
                  font=("Segoe UI", 11, "bold"), padx=20, relief=tk.FLAT).pack(side=tk.LEFT, padx=10)

    def update_grid(self):
        for widget in self.scrollable_frame.winfo_children(): widget.destroy()
        n = self.n_var.get()
        self.entries_a, self.entries_b = [], []
        for j in range(n):
            ttk.Label(self.scrollable_frame, text=f"x{j + 1}", font=("Arial", 10, "bold")).grid(row=0, column=j)
        ttk.Label(self.scrollable_frame, text="| B", font=("Arial", 10, "bold")).grid(row=0, column=n+1)

        for i in range(n):
            row_entries = []
            for j in range(n):
                ent = ttk.Entry(self.scrollable_frame, width=8, justify='center')
                ent.grid(row=i + 1, column=j, padx=2, pady=2)
                ent.insert(0, "0"); row_entries.append(ent)
            self.entries_a.append(row_entries)
            ent_b = ttk.Entry(self.scrollable_frame, width=8, justify='center', foreground="#c0392b")
            ent_b.grid(row=i + 1, column=n + 1, padx=2, pady=2)
            ent_b.insert(0, "0"); self.entries_b.append(ent_b)

    def clear_fields(self):
        for row in self.entries_a:
            for ent in row: ent.delete(0, tk.END); ent.insert(0, "0")
        for ent in self.entries_b: ent.delete(0, tk.END); ent.insert(0, "0")

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not file_path: return
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                n = int(lines[0].strip())
                self.n_var.set(n); self.update_grid()
                for i in range(n):
                    data = list(map(float, lines[i + 1].split()))
                    for j in range(n):
                        self.entries_a[i][j].delete(0, tk.END)
                        self.entries_a[i][j].insert(0, str(data[j]))
                    self.entries_b[i].delete(0, tk.END)
                    self.entries_b[i].insert(0, str(data[n]))
        except Exception as e: messagebox.showerror("Error", str(e))

    def solve(self):
        try:
            n = self.n_var.get()
            A = np.array([[float(e.get()) for e in row] for row in self.entries_a])
            B = np.array([float(e.get()) for e in self.entries_b])

            valid, det = solvers.is_matrix_valid(A)
            if not valid: raise ValueError(det)

            method = self.method_var.get()
            if method == "Cramer": X = solvers.solve_cramer(A, B)
            elif method == "Gauss": X = solvers.solve_gauss(A, B)
            elif method == "Gauss-Jordan": X = solvers.solve_gauss_jordan(A, B)
            elif method == "Jacobi": X = solvers.solve_jacobi(A, B)
            elif method == "Seidel": X = solvers.solve_seidel(A, B)

            correct = solvers.verify_solution(A, B, X)
            res = f"Method: {method} | det: {det:.2f}\n" + ", ".join([f"x{i+1}={v:.4f}" for i,v in enumerate(X)])
            self.lbl_result.config(text=f"{res}\n{'✅ Success' if correct else '❌ Error'}", fg="#2c3e50")
        except Exception as e: self.lbl_result.config(text=f"ERROR: {str(e)}", fg="#c0392b")