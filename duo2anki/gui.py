import tkinter as tk
from tkinter.constants import LEFT
import tkinter.ttk as ttk


class DuoWordsGui(tk.Frame):

    class DuoWordsListbox(tk.Listbox):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        padx, pady = 2, 2

        self._title = ttk.Label(self, text="Duolingo Words", font='-weight bold -size 10')
        self._title.pack(side=tk.TOP, fill=tk.X, padx=padx, pady=pady)

        self._chx_uncategorised = ttk.Checkbutton(self, text="Uncategorised only")
        self._chx_uncategorised.var = tk.IntVar()                                   # type: ignore
        self._chx_uncategorised.var.set(0)                                          # type: ignore
        self._chx_uncategorised.configure(variable=self._chx_uncategorised.var)     # type: ignore
        self._chx_uncategorised.pack(side=tk.TOP, fill=tk.X, padx=padx, pady=pady)

        sub_frame1 = tk.Frame(self)
        sub_frame1.pack(side=tk.TOP, fill=tk.X)

        self._lbl_filter = tk.Label(sub_frame1, text="Filter: ")
        self._lbl_filter.pack(side=tk.LEFT, padx=padx, pady=pady)

        self._tbx_filter = ttk.Entry(sub_frame1)
        self._tbx_filter.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=padx, pady=pady)

        self._lbx_words = DuoWordsGui.DuoWordsListbox(self)
        self._lbx_words.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=padx, pady=pady)


class AnkiWordsGui(tk.Frame):

    class AnkiWordsListbox(tk.Listbox): pass

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        padx, pady = 2, 2

        self._title = ttk.Label(self, text="Anki Words", font='-weight bold -size 10')
        self._title.pack(side=tk.TOP, fill=tk.X, padx=padx, pady=pady)

        self._chx_untranslated = ttk.Checkbutton(self, text="No translations only")
        self._chx_untranslated.var = tk.IntVar()                                   # type: ignore
        self._chx_untranslated.var.set(0)                                          # type: ignore
        self._chx_untranslated.configure(variable=self._chx_untranslated.var)     # type: ignore
        self._chx_untranslated.pack(side=tk.TOP, fill=tk.X, padx=padx, pady=pady)

        sub_frame1 = tk.Frame(self)
        sub_frame1.pack(side=tk.TOP, fill=tk.X)

        self._lbl_filter = tk.Label(sub_frame1, text="Filter: ")
        self._lbl_filter.pack(side=tk.LEFT, padx=padx, pady=pady)

        self._tbx_filter = ttk.Entry(sub_frame1)
        self._tbx_filter.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=padx, pady=pady)

        self._lbx_words = AnkiWordsGui.AnkiWordsListbox(self)
        self._lbx_words.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=padx, pady=pady)

class AnkiCardGui(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        padx, pady = 2, 2

        self._title = ttk.Label(self, text="Anki Words", font='-weight bold -size 10')
        self._title.pack(side=tk.TOP, fill=tk.X, padx=padx, pady=pady)


class Duo2AnkiGui(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._duo = DuoWordsGui(self)
        self._duo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._anki = AnkiWordsGui(self)
        self._anki.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._anki_card = AnkiCardGui(self)
        self._anki_card.pack(side=tk.LEFT, fill=tk.BOTH)


def main():
    root = tk.Tk()
    gui = Duo2AnkiGui(master=root)
    gui.pack(fill=tk.BOTH, expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()