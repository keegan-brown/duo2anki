from __future__ import annotations
import json
import os
from typing import List, Dict, Tuple, TypedDict, Optional
import uuid

class Model:

    PATH_MODELS = 'models/'

    class ModelTemplate(TypedDict):
        duo:    Dict[str, Optional[str]]
        anki:   Dict[str, Tuple[str, str]]

    @property
    def TEMPLATE(self) -> ModelTemplate:
        return {'duo': {}, 'anki': {}}

    def __init__(self, file):
        self._file = os.path.join(self.PATH_MODELS, file)
        self._json = self.TEMPLATE

        if not os.path.exists(self._file):
            self._create()
        self._read()

    def _create(self):
        os.makedirs(self.PATH_MODELS, exist_ok=True)
        if os.path.exists(self._file):
            raise PermissionError(f'File {self._file} already exists, cannot create.')
        self._json = self.TEMPLATE
        self._update()

    def _read(self):
        with open(self._file, 'r') as f:
            self._json = json.load(f)

    def _update(self):
        with open(self._file, 'w') as f:
            json.dump(self._json, f)

    def update_duo_words(self, file: str):
        '''Updates the model JSON file with newly learned Duolingo words.'''
        with open(file, 'r') as f:
            duo_vocab = json.load(f)

        for _word in duo_vocab['vocab_overview']:
            word = _word['word_string']
            if word not in self._json['duo']:
                self._json['duo'].update({word: None})

        self._update()

    def get_anki_key(self, anki_word: str) -> str:
        keys = [key for key in self._json['anki'] if self._json['anki'][key][0] == anki_word]

        if not len(keys):
            self._json['anki'].update({str(uuid.uuid4()): (anki_word, '')})
            self._update()
            return self.get_anki_key(anki_word)
            
        if len(keys) > 1:
            pass # TODO
        
        return keys[0]

    def assign_duo_word(self, duo_word: str, anki_word: str):
        anki_key = self.get_anki_key(anki_word)
        self._json['duo'].update({duo_word: anki_key})

        if anki_key not in self._json['anki']:
            self._json['anki'].update({anki_key: ('', '')})

        self._update()

    def get_duo_words(self, filter: str='', unassigned_only: bool=False) -> List[str]:
        start_matches = sorted([duo_word for duo_word, anki_key in self._json['duo'].items() if duo_word.lower().startswith(filter)])
        other_matches = sorted([anki_word for anki_key, (anki_word, translation) in self._json['anki'].items() if (anki_word not in start_matches) and (filter in anki_word.lower())])
        words = start_matches + other_matches
        if unassigned_only:
            words = [word for word in words if self._json['duo'][word] is None or self._json['duo'][word] not in self._json['anki']]
        return words

    def get_duo_words_from_anki_key(self, anki_key: str) -> List[str]:
        return [duo_word for duo_word, _anki_key in self._json['duo'].items() if anki_key == _anki_key]

    def get_anki_words(self, filter: str='') -> List[str]:
        start_matches = sorted([anki_word for anki_word, translation in self._json['anki'].values() if anki_word.lower().startswith(filter.lower())])
        other_matches = sorted([anki_word for anki_word, translation in self._json['anki'].values() if filter.lower() in anki_word.lower() and anki_word not in start_matches])
        return start_matches + other_matches

    def assign_anki_translation(self, anki_key: str, anki_word: str, translation: str):
        self._json['anki'].update({anki_key: (anki_word, translation)})
        self._update()

    def is_assigned(self, duo_word: str) -> bool:
        return self._json['duo'][duo_word] is not None and self._json['duo'][duo_word] in self._json['anki']

    def is_translated(self, anki_word: str) -> bool:
        return self._json['anki'][anki_word] is not None

    def export_anki_csv(self, file_out):
        pass

    def get_json(self) -> ModelTemplate:
        return self._json.copy()

