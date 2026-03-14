import tkinter as tk
from gui import SLAESolverApp


def main():
    root = tk.Tk()

    # Optional: Theme styling
    try:
        root.tk.call('source', 'azure.tcl')
        root.tk.call('set_theme', 'light')
    except:
        pass

    app = SLAESolverApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()