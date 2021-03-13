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

        ttk.Label(self, text="Duolingo Words", font='-weight bold -size 10').pack(side=tk.TOP, fill=tk.X, padx=PSMALL, pady=PSMALL)        

        self._chx_uncategorised = ttk.Checkbutton(self, text="Uncategorised only")
        self._chx_uncategorised.var = tk.IntVar(value=0)                            # type: ignore        
        self._chx_uncategorised.configure(variable=self._chx_uncategorised.var)     # type: ignore
        self._chx_uncategorised.pack(side=tk.TOP, fill=tk.X, padx=PSMALL, pady=PSMALL)

        sub_frame1 = tk.Frame(self)
        sub_frame1.pack(side=tk.TOP, fill=tk.X)

        tk.Label(sub_frame1, text="Filter: ").pack(side=tk.LEFT, padx=PSMALL, pady=PSMALL)        

        self._tbx_filter = ttk.Entry(sub_frame1)
        self._tbx_filter.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=PSMALL, pady=PSMALL)

        sub_frame2 = tk.Frame(self)
        sub_frame2.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=PSMALL, pady=PSMALL)

        self._lbx_words = DuoWordsGui.DuoWordsListbox(sub_frame2)
        self._lbx_words.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=PSMALL, pady=PSMALL)
        scroll = ttk.Scrollbar(sub_frame2, command=self._lbx_words.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self._lbx_words.configure(yscrollcommand=scroll.set)

    def refresh(self, json_data: ModelTemplate):
        pass


class AnkiWordsGui(tk.Frame):

    class AnkiWordsListbox(tk.Listbox): pass

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        ttk.Label(self, text="Anki Words", font='-weight bold -size 10').pack(side=tk.TOP, fill=tk.X, padx=PSMALL, pady=PSMALL)
        
        self._chx_untranslated = ttk.Checkbutton(self, text="No translations only")
        self._chx_untranslated.var = tk.IntVar(value=0)                         # type: ignore        
        self._chx_untranslated.configure(variable=self._chx_untranslated.var)   # type: ignore
        self._chx_untranslated.pack(side=tk.TOP, fill=tk.X, padx=PSMALL, pady=PSMALL)

        sub_frame1 = tk.Frame(self)
        sub_frame1.pack(side=tk.TOP, fill=tk.X)

        tk.Label(sub_frame1, text="Filter: ").pack(side=tk.LEFT, padx=PSMALL, pady=PSMALL)

        self._tbx_filter = ttk.Entry(sub_frame1)
        self._tbx_filter.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=PSMALL, pady=PSMALL)

        sub_frame2 = tk.Frame(self)
        sub_frame2.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=PSMALL, pady=PSMALL)

        self._lbx_words = AnkiWordsGui.AnkiWordsListbox(sub_frame2)
        self._lbx_words.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=PSMALL, pady=PSMALL)
        scroll = ttk.Scrollbar(sub_frame2, command=self._lbx_words.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self._lbx_words.configure(yscrollcommand=scroll.set)


    def refresh(self, json_data: ModelTemplate):
        pass

class AnkiCardGui(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        ttk.Label(self, text="Anki Card", font='-weight bold -size 10').grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=PSMALL, pady=PSMALL)
        
        ttk.Label(self, text="Front side:").grid(row=1, column=0, sticky=tk.E, padx=PSMALL, pady=PSMALL)

        self._tbx_front = ttk.Entry(self)
        self._tbx_front.grid(row=1, column=1, padx=PSMALL, pady=PSMALL)

        ttk.Label(self, text="Back side:").grid(row=2, column=0, sticky=tk.E, padx=PSMALL, pady=PSMALL)

        self._tbx_back = ttk.Entry(self)
        self._tbx_back.grid(row=2, column=1, padx=PSMALL, pady=PSMALL)

        ttk.Label(self, text="Tags:").grid(row=3, column=0, sticky=tk.NE, padx=PSMALL, pady=PSMALL)

        sub_frame1 = tk.Frame(self)
        sub_frame1.grid(row=3, column=1, sticky=tk.NSEW, padx=PSMALL, pady=PSMALL)

        self._tags = {
            'noun': ttk.Checkbutton(sub_frame1, text='Noun'),
            'verb': ttk.Checkbutton(sub_frame1, text='Verb'),
            'adjective': ttk.Checkbutton(sub_frame1, text='Adjective'),
        }

        for cbx in self._tags.values():
            cbx.var = tk.IntVar(value=0)    # type: ignore -> dynamic attribute
            cbx.configure(variable=cbx.var) # type: ignore -> dynamic attribute
            cbx.pack(side=tk.TOP, fill=tk.X, padx=PSMALL//2, pady=PSMALL//2)

        ttk.Separator(self, orient=tk.HORIZONTAL).grid(row=4, column=0, columnspan=2, sticky=tk.EW, padx=PSMALL, pady=PSMALL)

        ttk.Label(self, text="Linked Duolingo words:").grid(row=5, column=0, columnspan=2, sticky=tk.W, padx=PSMALL, pady=PSMALL)

        sub_frame2 = tk.Frame(self)
        sub_frame2.grid(row=6, column=0, columnspan=2, sticky=tk.NSEW, padx=PSMALL, pady=PSMALL)

        self._lbx_words = tk.Listbox(sub_frame2)
        self._lbx_words.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=PSMALL, pady=PSMALL)
        scroll = ttk.Scrollbar(sub_frame2, command=self._lbx_words.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self._lbx_words.configure(yscrollcommand=scroll.set)

        self.rowconfigure(index=6, weight=1)
        

class Duo2AnkiGui(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._model: Optional[Model] = None 
        self._setup_ui()
        

    def _setup_ui(self):

        self._duo = DuoWordsGui(self)
        self._duo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=PSMALL, pady=PSMALL)

        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=PBIG, pady=PBIG)

        self._anki = AnkiWordsGui(self)
        self._anki.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=PSMALL, pady=PSMALL)

        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=PBIG, pady=PBIG)

        self._anki_card = AnkiCardGui(self)
        self._anki_card.pack(side=tk.LEFT, fill=tk.BOTH, padx=PSMALL, pady=PSMALL)

        menu = tk.Menu(self)
        menu_file = tk.Menu(menu, tearoff=0)
        menu_file.add_command(label="Import Duolingo words ...")
        menu_file.add_command(label="Export Anki .csv ...")
        menu.add_cascade(label='File', menu=menu_file)
        self.master.configure(menu=menu) # type: ignore -> menu exists in root

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