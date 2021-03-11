import tkinter as tk
import tkinter.ttk as ttk


class DuoWordsGui(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._title = ttk.Label(self, text="Duolingo Words", font='-weight bold -size 10')
        self._title.pack(side=tk.TOP)

        self._chx_uncategorised = ttk.Checkbutton(self, text="Uncategorised only")
        self._chx_uncategorised.var = tk.IntVar()                                   # type: ignore
        self._chx_uncategorised.var.set(0)                                          # type: ignore
        self._chx_uncategorised.configure(variable=self._chx_uncategorised.var)     # type: ignore
        self._chx_uncategorised.pack()


class AnkiWordsGui(tk.Frame):
    pass


class Duo2AnkiGui(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._duo = DuoWordsGui(self)
        self._duo.pack(side=tk.LEFT)

        self._anki = AnkiWordsGui(self)
        self._anki.pack(side=tk.RIGHT)


def main():
    root = tk.Tk()
    gui = Duo2AnkiGui(master=root)
    gui.pack()

    root.mainloop()


if __name__ == "__main__":
    main()