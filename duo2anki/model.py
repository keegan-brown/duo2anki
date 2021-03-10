import json
import os
from typing import List


class Model:
    
    PATH_MODELS = 'models/'

    def __init__(self, file):
        self._file = os.path.join(self.PATH_MODELS, file)        

        if not os.path.exists(self._file):
            self._create()
        self._read()

    @staticmethod
    def _template():
        '''The file should be structured as follows:
        
        {
            'duo': {<duo_word>: <anki_key>, ...}
            'anki': {<anki_key>: [<anki_word>, <anki_translation>], ...}
        }
        '''
        return {
            'duo': {},
            'anki': {}
        }

    def _create(self):
        os.makedirs(self.PATH_MODELS, exist_ok=True)
        if os.path.exists(self._file):
            raise PermissionError(f'File {self._file} already exists, cannot create.')        
        self._json = Model._template()
        self._update()        

    def _read(self):
        with open(self._file, 'r') as f:
            self._json = json.load(f)

    def _update(self):        
        with open(self._file, 'w') as f:
            json.dump(self._json, f)            

    def update_duo_words(self, file: str) -> List[str]:
        '''Updates the model JSON file with newly learned Duolingo words.'''
        with open(file, 'r') as f:
            duo_vocab = json.load(f)

        for _word in duo_vocab['vocab_overview']:
            word = _word['word_string']
            if word not in self._json['duo']:
                self._json['duo'].update({word: None})

        self._update()

    def assign_duo_word(self, duo_word: str, anki_word: str):
        if duo_word not in self._json['duo']:
            raise KeyError(f"Duolingo word '{duo_word}' not recognised, import it first using update_duo_words().")

        self._json['duo'].update({duo_word: anki_word})

        if anki_word not in self._json['anki']:
            self._json['anki'].update({anki_word: None})

        self._update()

    def get_duo_words(self, filter: str='', unassigned_only: bool = False) -> List[str]:
        start_matches = sorted([duo_word for duo_word, anki_word in self._json['duo'].items() 
                                if (duo_word.lower().startswith(filter)) 
                                and ((anki_word is None) or (anki_word not in self._json['anki']) if unassigned_only else True)])
        other_matches = sorted([anki_word for anki_word, translation in self._json['anki'].items() 
                                if (anki_word not in start_matches) 
                                and (filter in anki_word.lower()) 
                                and ((anki_word is None) or (anki_word not in self._json['anki']) if unassigned_only else True)])
        return start_matches + other_matches

    def get_duo_words_from_anki_word(self, anki_word: str) -> List[str]:
        return [duo_word for duo_word, _anki_word in self._json['duo'].items() if anki_word == _anki_word]
    
    def get_anki_words(self, filter: str='', unassigned_only: bool = False) -> List[str]:
        start_matches = sorted([anki_word for anki_word, translation in self._json['anki'].items() 
                                if (anki_word.lower().startswith(filter)) 
                                and (translation is None if unassigned_only else True)])
        other_matches = sorted([anki_word for anki_word, translation in self._json['anki'].items() 
                                if (anki_word not in start_matches) 
                                and (filter in anki_word.lower()) 
                                and (translation is None if unassigned_only else True)])
        return start_matches + other_matches

    def assign_anki_translation(self, anki_word: str, translation: str):
        #if anki_word not in self._json['anki']:
        #    raise KeyError(f"Anki word '{anki_word} not recognised, assign it first using assign_duo_word()'")
        self._json['anki'].update({anki_word: translation})

        self._update()

    def is_assigned(self, duo_word: str) -> bool:
        return self._json['duo'][duo_word] is not None and self._json['duo'][duo_word] in self._json['anki']

    def is_translated(self, anki_word: str) -> bool:
        return self._json['anki'][anki_word] is not None

    def export_anki_csv(self, file_out):
        pass

    def get_json(self) -> dict:
        return self._json.copy()

