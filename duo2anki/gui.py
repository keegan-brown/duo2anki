import tkinter as tk
import tkinter.ttk as ttk
from typing import Optional


from duo2anki.model import Model, ModelTemplate

PBIG, PSMALL = 5, 2     # padding constants


class DuoWordsGui(tk.Frame):

    class DuoWordsListbox(tk.Listbox):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._title = ttk.Label(self, text="Duolingo Words", font='-weight bold -size 10')
        self._title.pack(side=tk.TOP, fill=tk.X, padx=PSMALL, pady=PSMALL)

        self._chx_uncategorised = ttk.Checkbutton(self, text="Uncategorised only")
        self._chx_uncategorised.var = tk.IntVar(value=0)                            # type: ignore        
        self._chx_uncategorised.configure(variable=self._chx_uncategorised.var)     # type: ignore
        self._chx_uncategorised.pack(side=tk.TOP, fill=tk.X, padx=PSMALL, pady=PSMALL)

        sub_frame1 = tk.Frame(self)
        sub_frame1.pack(side=tk.TOP, fill=tk.X)

        self._lbl_filter = tk.Label(sub_frame1, text="Filter: ")
        self._lbl_filter.pack(side=tk.LEFT, padx=PSMALL, pady=PSMALL)

        self._tbx_filter = ttk.Entry(sub_frame1)
        self._tbx_filter.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=PSMALL, pady=PSMALL)

        self._lbx_words = DuoWordsGui.DuoWordsListbox(self)
        self._lbx_words.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=PSMALL, pady=PSMALL)

    def refresh(self, json_data: ModelTemplate):
        pass


class AnkiWordsGui(tk.Frame):

    class AnkiWordsListbox(tk.Listbox): pass

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._title = ttk.Label(self, text="Anki Words", font='-weight bold -size 10')
        self._title.pack(side=tk.TOP, fill=tk.X, padx=PSMALL, pady=PSMALL)

        self._chx_untranslated = ttk.Checkbutton(self, text="No translations only")
        self._chx_untranslated.var = tk.IntVar(value=0)                         # type: ignore        
        self._chx_untranslated.configure(variable=self._chx_untranslated.var)   # type: ignore
        self._chx_untranslated.pack(side=tk.TOP, fill=tk.X, padx=PSMALL, pady=PSMALL)

        sub_frame1 = tk.Frame(self)
        sub_frame1.pack(side=tk.TOP, fill=tk.X)

        self._lbl_filter = tk.Label(sub_frame1, text="Filter: ")
        self._lbl_filter.pack(side=tk.LEFT, padx=PSMALL, pady=PSMALL)

        self._tbx_filter = ttk.Entry(sub_frame1)
        self._tbx_filter.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=PSMALL, pady=PSMALL)

        self._lbx_words = AnkiWordsGui.AnkiWordsListbox(self)
        self._lbx_words.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=PSMALL, pady=PSMALL)

    def refresh(self, json_data: ModelTemplate):
        pass

class AnkiCardGui(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._tags = {
            'noun': ttk.Checkbutton(self, text='Noun'),
            'verb': ttk.Checkbutton(self, text='Verb'),
            'adjective': ttk.Checkbutton(self, text='Adjective'),
        }
        
        ttk.Label(self, text="Anki Card", font='-weight bold -size 10').grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=PSMALL, pady=PSMALL)
        ttk.Label(self, text="Front side:").grid(row=1, column=0, sticky=tk.E, padx=PSMALL, pady=PSMALL)
        ttk.Label(self, text="Back side:").grid(row=2, column=0, sticky=tk.E, padx=PSMALL, pady=PSMALL)
        ttk.Label(self, text="Tags:").grid(row=3, column=0, sticky=tk.E, padx=PSMALL, pady=PSMALL)
        ttk.Separator(self, orient=tk.HORIZONTAL).grid(row=3+len(self._tags), column=0, columnspan=2, sticky=tk.EW, padx=PSMALL, pady=PSMALL)
        ttk.Label(self, text="Linked Duolingo words:").grid(row=4+len(self._tags), column=0, columnspan=2, sticky=tk.W, padx=PSMALL, pady=PSMALL)

        self._tbx_front = ttk.Entry(self)
        self._tbx_front.grid(row=1, column=1, padx=PSMALL, pady=PSMALL)

        self._tbx_back = ttk.Entry(self)
        self._tbx_back.grid(row=2, column=1, padx=PSMALL, pady=PSMALL)

        for i, check in enumerate(self._tags.values()):
            check.var = tk.IntVar(value=0)          # type: ignore -> dynamic attribute
            check.configure(variable=check.var)     # type: ignore -> dynamic attribute
            check.grid(row=3 + i, column=1, sticky=tk.W, padx=PSMALL, pady=PSMALL)

        self._lbx_words = tk.Listbox(self)
        self._lbx_words.grid(row=5+len(self._tags), column=0, columnspan=2, sticky=tk.NSEW, padx=PSMALL, pady=PSMALL)

        self.rowconfigure(index=5+len(self._tags), weight=1)
        

class Duo2AnkiGui(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._model: Optional[Model] = None 

        self._duo = DuoWordsGui(self)
        self._duo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=PSMALL, pady=PSMALL)

        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=PBIG, pady=PBIG)

        self._anki = AnkiWordsGui(self)
        self._anki.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=PSMALL, pady=PSMALL)

        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=PBIG, pady=PBIG)

        self._anki_card = AnkiCardGui(self)
        self._anki_card.pack(side=tk.LEFT, fill=tk.BOTH, padx=PSMALL, pady=PSMALL)

    def refresh(self):
        json_data = self._model.get_json()
        self._duo.refresh(json_data)
        self._anki.refresh(json_data)
        

def main():
    root = tk.Tk()
    gui = Duo2AnkiGui(master=root)
    gui.pack(fill=tk.BOTH, expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()