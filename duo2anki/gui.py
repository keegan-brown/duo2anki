import os
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
from typing import Optional, Tuple

from duo2anki.model import Model, ModelInfo, ModelDict


PBIG, PSMALL = 5, 2     # padding constants


class DuoWordsGui(tk.Frame):

    class DuoWordsListbox(tk.Listbox):
        pass

    def __init__(self, *args, model=None, **kwargs):
        super().__init__(*args, **kwargs)

        self._model: Optional[Model] = model
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):

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

    def refresh(self):
        pass


class AnkiWordsGui(tk.Frame):

    class AnkiWordsListbox(tk.Listbox): pass

    def __init__(self, *args, model=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._model: Optional[Model] = model
        self._setup_ui()
        self.refresh()    

    def _setup_ui(self):
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

    def refresh(self):
        pass

class AnkiCardGui(tk.Frame):
    def __init__(self, *args, model=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._model: Optional[Model] = model
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
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
        
    def refresh(self):
        pass


class Gui(tk.Frame):

    class _NewDatabaseGui(tk.Toplevel):

        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)

            self._db_info: ModelInfo = {'name': '', 'lang': ''}
            self._db_path: str = ''

            self._setup_ui()

        def _setup_ui(self):

            ttk.Label(self, text='Database Name:').grid(row=0, column=0, sticky=tk.E, padx=PSMALL, pady=PSMALL)            
            self._db_name = tk.StringVar()            
            ttk.Entry(self, textvariable=self._db_name).grid(row=0, column=1, sticky=tk.EW, padx=PSMALL, pady=PSMALL)

            ttk.Label(self, text='Language:').grid(row=1, column=0, sticky=tk.E, padx=PSMALL, pady=PSMALL)
            self._lang = tk.StringVar()
            ttk.Entry(self, textvariable=self._lang).grid(row=1, column=1, sticky=tk.EW, padx=PSMALL, pady=PSMALL)

            ttk.Label(self, text='Filename:').grid(row=2, column=0, sticky=tk.E, padx=PSMALL, pady=PSMALL)
            self._file = tk.StringVar()
            ttk.Entry(self, textvariable=self._file).grid(row=2, column=1, sticky=tk.EW, padx=PSMALL, pady=PSMALL)

            ttk.Label(self, text='Directory:').grid(row=3, column=0, sticky=tk.E, padx=PSMALL, pady=PSMALL)
            self._path = tk.StringVar()
            ttk.Entry(self, textvariable=self._path).grid(row=3, column=1, sticky=tk.EW, padx=PSMALL, pady=PSMALL)

            ttk.Button(self, text='...', width=8, command=self.get_dir).grid(row=3, column=2, padx=PSMALL, pady=PSMALL)            

            sub_frame1 = tk.Frame(self)
            sub_frame1.grid(row=4, column=0, columnspan=3, sticky=tk.EW)

            ttk.Button(sub_frame1, command=self.cancel, text='Cancel').pack(side=tk.RIGHT)
            ttk.Button(sub_frame1, command=self.ok, text='Ok').pack(side=tk.RIGHT)

            self.columnconfigure(index=1, weight=1)

        def ok(self):
            valid, msg = self.validate()
            if not valid:
                messagebox.showerror('Error', msg)
            self._db_info = {
                'name': self._db_name.get(),
                'lang': self._lang.get(),
            }
            self._db_path = os.path.join(self._path.get(), self._file.get())
            self.destroy()

        def cancel(self):
            self.destroy()

        def validate(self) -> Tuple[bool, str]:
            return True, ''

        def get_new_db_info(self) -> Tuple[ModelInfo, str]:
            self.grab_set()
            self.wait_window()
            return self._db_info, self._db_path


        def get_dir(self) -> None:
            res = filedialog.askdirectory()
            if res:
                self._path.set(res)
            self.deiconify()

    def __init__(self, *args, model=None, **kwargs):
        super().__init__(*args, **kwargs)

        self._model: Optional[Model] = model 
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):

        self.master.geometry('900x600') # type: ignore -> root has geometry() method

        self._duo = DuoWordsGui(self)
        self._duo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=PSMALL, pady=PSMALL)

        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=PBIG, pady=PBIG)

        self._anki = AnkiWordsGui(self)
        self._anki.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=PSMALL, pady=PSMALL)

        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=PBIG, pady=PBIG)

        self._anki_card = AnkiCardGui(self)
        self._anki_card.pack(side=tk.LEFT, fill=tk.BOTH, padx=PSMALL, pady=PSMALL)

        # Menu bar
        menu = tk.Menu(self)

        ni = lambda: messagebox.showerror('Error:', 'This feature is not yet implemented!')

        menu_file = tk.Menu(menu, tearoff=0)
        menu_file.add_command(label="New Database", command=self.cmd_new_database)
        menu_file.add_command(label="Open Database", command=ni)
        menu_file.add_command(label="Save Database As", command=ni)
        menu.add_cascade(label='File', menu=menu_file)

        menu_duo = tk.Menu(menu, tearoff=0)
        menu_duo.add_command(label="Import Duolingo words from Clipboard", command=ni)
        menu.add_cascade(label='Duolingo', menu=menu_duo)

        menu_anki = tk.Menu(menu, tearoff=0)
        menu_anki.add_command(label="Export Anki words to file", command=ni)
        menu.add_cascade(label='Anki', menu=menu_anki)

        self.master.configure(menu=menu) # type: ignore -> menu exists in root

    def refresh(self):
        for component in (self._duo, self._anki, self._anki_card):
            component.refresh()

    def cmd_new_database(self):
        '''Creates a new database.'''        
        db_info, path = Gui._NewDatabaseGui(self).get_new_db_info()
        pass
        

def main():
    root = tk.Tk()
    gui = Gui(master=root)
    gui.pack(fill=tk.BOTH, expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()