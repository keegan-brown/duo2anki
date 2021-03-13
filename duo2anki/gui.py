import os
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
from typing import Dict, Optional, Tuple

from duo2anki.model import Model, ModelInfo, ModelDict


PBIG, PSMALL = 5, 2     # padding constants


class DuoWordsGui(tk.Frame):

    def __init__(self, *args, model=None, **kwargs):
        super().__init__(*args, **kwargs)

        self._model: Optional[Model] = model
        self._setup_ui()
        self.refresh(model)

    def _setup_ui(self):
        
        ttk.Label(self, text="Duolingo Words", font='-weight bold -size 10').pack(side=tk.TOP, fill=tk.X, padx=PSMALL, pady=PSMALL)  

        self._uncategorised = tk.IntVar(value=0)
        ttk.Checkbutton(self, text="Uncategorised only", variable=self._uncategorised).pack(side=tk.TOP, fill=tk.X, padx=PSMALL, pady=PSMALL)

        sub_frame1 = tk.Frame(self)
        sub_frame1.pack(side=tk.TOP, fill=tk.X)

        tk.Label(sub_frame1, text="Filter: ").pack(side=tk.LEFT, padx=PSMALL, pady=PSMALL)
        self._filter_text = tk.StringVar()
        ttk.Entry(sub_frame1, textvariable=self._filter_text).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=PSMALL, pady=PSMALL)

        sub_frame2 = tk.Frame(self)
        sub_frame2.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=PSMALL, pady=PSMALL)

        self._lbx_words = tk.Listbox(sub_frame2)
        self._lbx_words.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=PSMALL, pady=PSMALL)
        scroll = ttk.Scrollbar(sub_frame2, command=self._lbx_words.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self._lbx_words.configure(yscrollcommand=scroll.set)

    def refresh(self, model: Optional[Model]):
        self._model = model

        if self._model:
            pass

    


class AnkiWordsGui(tk.Frame):

    def __init__(self, *args, model=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._model: Optional[Model] = None
        self._setup_ui()
        self.refresh(model)    

    def _setup_ui(self):

        ttk.Label(self, text="Anki Words", font='-weight bold -size 10').pack(side=tk.TOP, fill=tk.X, padx=PSMALL, pady=PSMALL)
        
        self._untranslated = tk.IntVar()
        ttk.Checkbutton(self, text="No translations only", variable=self._untranslated).pack(side=tk.TOP, fill=tk.X, padx=PSMALL, pady=PSMALL)

        sub_frame1 = tk.Frame(self)
        sub_frame1.pack(side=tk.TOP, fill=tk.X)

        tk.Label(sub_frame1, text="Filter: ").pack(side=tk.LEFT, padx=PSMALL, pady=PSMALL)
        self._filter_text = tk.StringVar()
        ttk.Entry(sub_frame1, textvariable=self._filter_text).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=PSMALL, pady=PSMALL)

        sub_frame2 = tk.Frame(self)
        sub_frame2.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=PSMALL, pady=PSMALL)

        self._lbx_words = tk.Listbox(sub_frame2)
        self._lbx_words.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=PSMALL, pady=PSMALL)
        scroll = ttk.Scrollbar(sub_frame2, command=self._lbx_words.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self._lbx_words.configure(yscrollcommand=scroll.set)

    def refresh(self, model: Optional[Model]):
        pass


class AnkiCardGui(tk.Frame):
    def __init__(self, *args, model=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._model: Optional[Model] = None
        self._setup_ui()
        self.refresh(model)

    def _setup_ui(self):

        ttk.Label(self, text="Anki Card", font='-weight bold -size 10').grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=PSMALL, pady=PSMALL)
        
        ttk.Label(self, text="Front side:").grid(row=1, column=0, sticky=tk.E, padx=PSMALL, pady=PSMALL)

        self._front = tk.StringVar()
        ttk.Entry(self, textvariable=self._front).grid(row=1, column=1, padx=PSMALL, pady=PSMALL)

        ttk.Label(self, text="Back side:").grid(row=2, column=0, sticky=tk.E, padx=PSMALL, pady=PSMALL)

        self._back = tk.StringVar()
        ttk.Entry(self, textvariable=self._back).grid(row=2, column=1, padx=PSMALL, pady=PSMALL)

        ttk.Label(self, text="Tags:").grid(row=3, column=0, sticky=tk.NE, padx=PSMALL, pady=PSMALL)

        sub_frame1 = tk.Frame(self)
        sub_frame1.grid(row=3, column=1, sticky=tk.NSEW, padx=PSMALL, pady=PSMALL)

        self._tags: Dict[str, tk.Variable] = {
            'noun': tk.IntVar(value=0),
            'verb': tk.IntVar(value=0),
            'adjective': tk.IntVar(value=0),
        }

        for key, value in self._tags.items():
            ttk.Checkbutton(sub_frame1, variable=value, text=key.capitalize()).pack(side=tk.TOP, fill=tk.X, padx=PSMALL//2, pady=PSMALL//2)

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
        
    def refresh(self, model: Optional[Model]):
        pass


class Gui(tk.Frame):

    class _DialogNewDb(tk.Toplevel):

        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)

            self._db_info: Optional[ModelInfo] = None
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
            self._dir = tk.StringVar()
            ttk.Entry(self, textvariable=self._dir).grid(row=3, column=1, sticky=tk.EW, padx=PSMALL, pady=PSMALL)

            ttk.Button(self, text='...', width=8, command=self._get_dir).grid(row=3, column=2, padx=PSMALL, pady=PSMALL)            

            sub_frame1 = tk.Frame(self)
            sub_frame1.grid(row=4, column=0, columnspan=3, sticky=tk.EW)

            ttk.Button(sub_frame1, command=self.cancel, text='Cancel').pack(side=tk.RIGHT)
            ttk.Button(sub_frame1, command=self.ok, text='Ok').pack(side=tk.RIGHT)

            self.columnconfigure(index=1, weight=1)

        def _validate(self) -> Tuple[bool, str]:
            if self._db_name.get() == '':
                return False, 'Database name not given'
            if self._lang.get() == '':
                return False, 'Language not specified'
            if self._file.get() == '':
                return False, 'Filename not specified'
            if self._dir.get() == '':
                return False, 'Directory not chosen'
            return True, ''

        def _get_dir(self) -> None:
            res = filedialog.askdirectory()
            if res:
                self._dir.set(os.path.normpath(res))
            self.deiconify()

        def ok(self):
            valid, msg = self._validate()
            if not valid:
                messagebox.showerror('Error', msg)
                return

            self._db_info = {
                'name': self._db_name.get(),
                'lang': self._lang.get(),
            }
            self._db_path = os.path.join(self._dir.get(), self._file.get())
            self.destroy()

        def cancel(self):
            self.destroy()

        def get_new_db_info(self) -> Tuple[Optional[ModelInfo], str]:
            self.grab_set()
            self.wait_window()
            return self._db_info, self._db_path

    def __init__(self, *args, model=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.root: tk.Tk = self.master # type: ignore -> should be called with root

        self._model: Optional[Model] = model 
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):

        self.root.geometry('900x600') 

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
        menu_file.add_command(label="Open Database", command=self.cmd_open_database)
        menu_file.add_command(label="Save Database As", command=ni)
        menu.add_cascade(label='File', menu=menu_file)

        menu_duo = tk.Menu(menu, tearoff=0)
        menu_duo.add_command(label="Import Duolingo words from Clipboard", command=ni)
        menu.add_cascade(label='Duolingo', menu=menu_duo)

        menu_anki = tk.Menu(menu, tearoff=0)
        menu_anki.add_command(label="Export Anki words to file", command=ni)
        menu.add_cascade(label='Anki', menu=menu_anki)

        self.root.configure(menu=menu) 

    def refresh(self):
        if self._model:
            self.root.title(f"Duo2Anki - {self._model.json['info']['name']}") 
        else:
            self.root.title("Duo2Anki") 

        for component in (self._duo, self._anki, self._anki_card):
            component.refresh(self._model)

    def cmd_new_database(self):
        '''Creates a new database.'''        
        info, path = Gui._DialogNewDb(self).get_new_db_info()
        if info:
            self._model = Model(path)
            self._model.update_info(info)
        self.refresh()

    def cmd_open_database(self):
        '''Opens an existing database.'''
        path = os.path.normpath(filedialog.askopenfilename())
        if path:
            try:
                self._model = Model(path)
            except Model.ModelError:
                messagebox.showerror('Error', f"Could not open file at '{path}', bad file format.")
        self.refresh()
        

def main():
    root = tk.Tk()
    gui = Gui(master=root)
    gui.pack(fill=tk.BOTH, expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()