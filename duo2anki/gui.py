from io import StringIO
import os
import tkinter as tk
import tkinter.dnd as dnd
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
from typing import Dict, List, Optional, Tuple

from duo2anki.model import Model, ModelInfo, ModelDict

PBIG, PSMALL = 5, 2     # padding constants

NI = lambda: messagebox.showerror('Error:', 'This feature is not yet implemented!')

class _DndListbox(tk.Listbox):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.bind('<Button-3>', self.on_drag_start)
        self.drop: Optional[_DndListbox] = None

    def dnd_accept(self, source, event):        
        return self

    def dnd_enter(self, source, event):        
        pass

    def dnd_motion(self, source, event):
        pass

    def dnd_leave(self, source, event):
        pass

    def dnd_end(self, target, event):
        if target is not None and self is not target:
            target.drop = self
            target.event_generate('<<DropReceived>>', when='tail')

    def dnd_commit(self, source, event):
        pass

    def on_drag_start(self, event):
        dnd.dnd_start(self, event)
    

class DuoWordsGui(tk.Frame):

    def __init__(self, *args, model=None, **kwargs):
        super().__init__(*args, **kwargs)

        self._model: Optional[Model] = model
        self._last_selected: List[str] = []
        self._setup_ui()
        self.refresh(model)

    def _setup_ui(self):
        
        ttk.Label(self, text="Duolingo Words", font='-weight bold -size 10').pack(side=tk.TOP, fill=tk.X, padx=PSMALL, pady=PSMALL)  

        self._uncategorised = tk.IntVar(value=0)
        ttk.Checkbutton(self, text="Uncategorised only", variable=self._uncategorised).pack(side=tk.TOP, fill=tk.X, padx=PSMALL, pady=PSMALL)
        self._uncategorised.trace_add('write', self._request_refresh)

        sub_frame1 = tk.Frame(self)
        sub_frame1.pack(side=tk.TOP, fill=tk.X)

        tk.Label(sub_frame1, text="Filter: ").pack(side=tk.LEFT, padx=PSMALL, pady=PSMALL)
        self._filter_text = tk.StringVar()
        self._tbx_filter_text = ttk.Entry(sub_frame1, textvariable=self._filter_text)
        self._tbx_filter_text.bind()
        self._tbx_filter_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=PSMALL, pady=PSMALL)
        self._filter_text.trace_add('write', self._request_refresh)

        sub_frame2 = tk.Frame(self)
        sub_frame2.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=PSMALL, pady=PSMALL)

        self._lbx_words = _DndListbox(sub_frame2, selectmode=tk.EXTENDED, exportselection=False)
        self._lbx_words.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=PSMALL, pady=PSMALL)
        self._lbx_words.bind('<<ListboxSelect>>', self._on_word_select)
        self._lbx_words.bind('<Key>', self._on_lbx_words_key)
        self._lbx_words.bind('<Button-3>', lambda e: self.event_generate('<<LinkWords>>', when='tail'))
        scroll = ttk.Scrollbar(sub_frame2, command=self._lbx_words.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self._lbx_words.configure(yscrollcommand=scroll.set)

    def refresh(self, model: Optional[Model] = None):
        self._model = model

        if self._model:
            self._lbx_words.delete(0, tk.END)

            for word in self._model.get_duo_words(self._filter_text.get(), bool(self._uncategorised.get())):
                self._lbx_words.insert(tk.END, word)
                if self._model.get_anki_key_from_duo_word(word):
                    self._lbx_words.itemconfig(tk.END, foreground='#266e16')
                else:
                    self._lbx_words.itemconfig(tk.END, foreground='#6e1616')

                if word in self._last_selected:
                    self._lbx_words.selection_set(tk.END)

    def get_selected_words(self) -> List[str]:
        return [self._lbx_words.get(i) for i in self._lbx_words.curselection()]

    def _request_refresh(self, *args):
        self.event_generate('<<RefreshRequired>>', when='tail')

    def _on_word_select(self, event):
        self._last_selected = self.get_selected_words()

    def _on_lbx_words_key(self, event):
        if event.keysym == 'Delete' and self.get_selected_words():
            if messagebox.askyesno('Delete?', 'Do you want to delete the selected Anki card?'):
                for word in self.get_selected_words():
                    self._model.delete_duo_word(word)
                self._request_refresh()


class AnkiWordsGui(tk.Frame):

    def __init__(self, *args, model=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._model: Optional[Model] = None
        self._last_selected: List[str] = []
        self._setup_ui()
        self.refresh(model)    

    def _setup_ui(self):

        ttk.Label(self, text="Anki Words", font='-weight bold -size 10').pack(side=tk.TOP, fill=tk.X, padx=PSMALL, pady=PSMALL)
        
        self._untranslated = tk.IntVar()
        ttk.Checkbutton(self, text="No translations only", variable=self._untranslated).pack(side=tk.TOP, fill=tk.X, padx=PSMALL, pady=PSMALL)
        self._untranslated.trace_add('write', self._request_refresh)

        sub_frame1 = tk.Frame(self)
        sub_frame1.pack(side=tk.TOP, fill=tk.X)

        tk.Label(sub_frame1, text="Filter: ").pack(side=tk.LEFT, padx=PSMALL, pady=PSMALL)
        self._filter_text = tk.StringVar()
        tbx_filter = ttk.Entry(sub_frame1, textvariable=self._filter_text)
        tbx_filter.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=PSMALL, pady=PSMALL)
        tbx_filter.bind('<Key>', self._on_filter_text_key)
        self._filter_text.trace_add('write', self._request_refresh)

        sub_frame2 = tk.Frame(self)
        sub_frame2.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=PSMALL, pady=PSMALL)

        self._lbx_words = _DndListbox(sub_frame2, exportselection=False)
        self._lbx_words.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=PSMALL, pady=PSMALL)
        self._lbx_words.bind('<<ListboxSelect>>', self._on_word_select)
        self._lbx_words.bind('<Button-3>', lambda e: self.event_generate('<<LinkWords>>', when='tail'))
        scroll = ttk.Scrollbar(sub_frame2, command=self._lbx_words.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self._lbx_words.configure(yscrollcommand=scroll.set)

        # events
        self._lbx_words.bind('<Key>', self._on_lbx_words_key)

    def refresh(self, model: Optional[Model]):
        self._model = model

        if self._model:
            self._lbx_words.delete(0, tk.END)

            for word in self._model.get_anki_words(filter=self._filter_text.get(), no_translation_only=bool(self._untranslated.get())):
                self._lbx_words.insert(tk.END, word)

                if self._model.get_duo_words_from_anki_word(word):
                    self._lbx_words.itemconfig(tk.END, foreground='#266e16')

                if word in self._last_selected:
                    self._lbx_words.selection_set(tk.END)

    def get_selected_words(self) -> List[str]:
        return [self._lbx_words.get(i) for i in self._lbx_words.curselection()]

        if duo_words:
            for duo_word in duo_words:
                self._model.link_duo_word_to_anki_word(duo_word, anki_word)

        self._request_refresh()

    def _on_word_select(self, event):
        self._last_selected = [self._lbx_words.get(i) for i in self._lbx_words.curselection()]
        self.event_generate('<<WordSelected>>', when='tail')

    def _on_lbx_words_key(self, event):
        if event.keysym == 'Delete' and self.get_selected_words():
            if messagebox.askyesno('Delete?', 'Do you want to delete the selected Anki card?'):
                for word in self.get_selected_words():
                    self._model.delete_anki_entry(self._model.get_anki_key_from_anki_word(word))
                self._request_refresh()

    def _on_filter_text_key(self, event):
        if event.keysym == 'Return' and self._filter_text.get() != '':
            if messagebox.askyesno('Add?', 'Do you want to add a new Anki card?'):
                self._model.get_anki_key_from_anki_word(self._filter_text.get())
                self._request_refresh()

    def _request_refresh(self, *args):
        self.event_generate('<<RefreshRequired>>', when='tail')


class AnkiCardGui(tk.Frame):
    def __init__(self, *args, model=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._model: Optional[Model] = None
        self._anki_word: str = ''
        self._setup_ui()
        self.refresh(model)

    def _setup_ui(self):

        ttk.Label(self, text="Anki Card", font='-weight bold -size 10').grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=PSMALL, pady=PSMALL)
        
        ttk.Label(self, text="Front side:").grid(row=1, column=0, sticky=tk.E, padx=PSMALL, pady=PSMALL)

        self._front = tk.StringVar()
        tbx_front = ttk.Entry(self, textvariable=self._front)
        tbx_front.grid(row=1, column=1, padx=PSMALL, pady=PSMALL)
        tbx_front.bind('<Key>', self._on_tbx_key)

        ttk.Label(self, text="Back side:").grid(row=2, column=0, sticky=tk.E, padx=PSMALL, pady=PSMALL)

        self._back = tk.StringVar()
        tbx_back = ttk.Entry(self, textvariable=self._back)
        tbx_back.grid(row=2, column=1, padx=PSMALL, pady=PSMALL)
        tbx_back.bind('<Key>', self._on_tbx_key)

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
        self._lbx_words.bind('<Key>', self._on_lbx_words_key)

        self.rowconfigure(index=6, weight=1)
        
    def refresh(self, model: Optional[Model], anki_words=[]):
        self._model = model
        self.clear()
        self.on_card_select(anki_words)

    def clear(self):
        self._front.set('')
        self._back.set('')
        self._lbx_words.delete(0, tk.END)

    def on_card_select(self, anki_words: List[str]):
        if not anki_words:
            self.clear()
            return

        self._anki_word, = anki_words
        duo_words = self._model.get_duo_words_from_anki_word(self._anki_word)
        anki_entry = self._model.get_anki_entry(self._model.get_anki_key_from_anki_word(self._anki_word))

        self._front.set(anki_entry[0])
        self._back.set(anki_entry[1])

        self._lbx_words.delete(0, tk.END)

        for word in duo_words:
            self._lbx_words.insert(tk.END, word)

    def get_selected_words(self) -> List[str]:
        return [self._lbx_words.get(i) for i in self._lbx_words.curselection()]

    def _on_tbx_key(self, event):
        if event.keysym == 'Return':
            key = self._model.get_anki_key_from_anki_word(self._anki_word)
            self._model.update_anki_entry(key, self._front.get(), self._back.get())
            self._anki_word = self._model.get_anki_entry(key)[0]
            self._request_refresh()

    def _on_lbx_words_key(self, event):
        if event.keysym == 'Delete' and self.get_selected_words():
            for duo_word in self.get_selected_words():
                self._model.unlink_duo_word(duo_word)
            self._request_refresh()

    def _request_refresh(self, *args):
        self.event_generate('<<RefreshRequired>>', when='tail')

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

        self._duo.bind('<<RefreshRequired>>', self.refresh)
        self._duo.bind('<<LinkWords>>', self.link_words)
        self._anki.bind('<<RefreshRequired>>', self.refresh)
        self._anki.bind('<<LinkWords>>', self.link_words)
        self._anki.bind('<<WordSelected>>', lambda e: self._anki_card.on_card_select(self._anki.get_selected_words()))
        self._anki_card.bind('<<RefreshRequired>>', self.refresh)

        # Menu bar
        menu = tk.Menu(self)        

        menu_file = tk.Menu(menu, tearoff=0)
        menu_file.add_command(label="New Database", command=self.cmd_new_database)
        menu_file.add_command(label="Open Database", command=self.cmd_open_database)
        menu_file.add_command(label="Save Database As", command=NI)
        menu.add_cascade(label='File', menu=menu_file)

        menu_duo = tk.Menu(menu, tearoff=0)
        menu_duo.add_command(label="Import Duolingo words from Clipboard", command=self.cmd_import_duo_words)
        menu.add_cascade(label='Duolingo', menu=menu_duo)

        menu_anki = tk.Menu(menu, tearoff=0)
        menu_anki.add_command(label="Export Anki words to file", command=self.cmd_export_anki_words)
        menu.add_cascade(label='Anki', menu=menu_anki)

        self.root.configure(menu=menu) 

    def refresh(self, *args):
        if self._model:
            self.root.title(f"Duo2Anki - {self._model.json['info']['name']}") 
        else:
            self.root.title("Duo2Anki") 
        
        self._duo.refresh(self._model)
        self._anki.refresh(self._model)
        self._anki_card.refresh(self._model, self._anki.get_selected_words())

    def link_words(self, event):
        duo_words = self._duo.get_selected_words()
        anki_words = self._anki.get_selected_words()

        if duo_words and anki_words:
            anki_word, = anki_words
            for duo_word in duo_words:
                self._model.link_duo_word_to_anki_word(duo_word, anki_word)
        self.refresh()

    def cmd_new_database(self):
        '''Creates a new database.'''        
        info, path = Gui._DialogNewDb(self).get_new_db_info()
        if info:
            self._model = Model(path)
            self._model.update_model_info(info)
        self.refresh()

    def cmd_open_database(self):
        '''Opens an existing database.'''
        path = os.path.normpath(filedialog.askopenfilename())
        if path != '.':
            try:
                self._model = Model(path)
            except Model.ModelError:
                messagebox.showerror('Error', f"Could not open file at '{path}', bad file format.")
        self.refresh()

    def cmd_import_duo_words(self):
        try:      
            self._model.update_duo_new_words_from_str(self.root.clipboard_get())
        except Exception as e:
            messagebox.showerror('Error', f'Something went wrong:\n{str(e)}')
        messagebox.showinfo('Info', 'Import successful!')
        self.refresh()
        
    def cmd_export_anki_words(self):
        path = os.path.normpath(filedialog.asksaveasfilename())
        if path != '.':
            try:
                self._model.export_anki_csv(path)
            except Model.ModelError:
                messagebox.showerror('Error', f"Could not export file at '{path}'")
        self.refresh()

def main():
    root = tk.Tk()
    gui = Gui(master=root)
    gui.pack(fill=tk.BOTH, expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()