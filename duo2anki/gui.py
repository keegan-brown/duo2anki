import tkinter as tk
import tkinter.ttk as ttk


class Duo2AnkiGui(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def main():
    root = tk.Tk()
    gui = Duo2AnkiGui(master=root)
    gui.pack()

    root.mainloop()


if __name__ == "__main__":
    main()