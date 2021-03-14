from __future__ import annotations
import json
from json.decoder import JSONDecodeError
import os
from pathlib import Path
from typing import List, Dict, Tuple, TypedDict, Optional
import uuid


class ModelInfo(TypedDict):
    name: str
    lang: str


class ModelDict(TypedDict):
    info:   ModelInfo
    duo:    Dict[str, Optional[str]]
    anki:   Dict[str, Tuple[str, str]]


class Model:

    class ModelError(Exception): pass

    @property
    def TEMPLATE(self) -> ModelDict:
        return {
            'info': {
                'name': '',
                'lang': '',
            },
            'duo': {}, 
            'anki': {},
            }

    @property
    def json(self) -> ModelDict:
        return self._json.copy()

    def __init__(self, file: str):
        self._file = Path(file)
        self._json: ModelDict = self.TEMPLATE
        if not os.path.exists(self._file):
            self._create()
        self._read()

    def _create(self):        
        if self._file.exists():
            raise PermissionError(f'File {self._file} already exists, cannot create.')
        self._file.touch(0o664)
        self._json = self.TEMPLATE
        self._update()

    def _read(self):
        with open(self._file, 'r') as f:
            try:
                self._json = json.load(f)
            except JSONDecodeError:
                raise Model.ModelError('Invalid File')


    def _update(self):
        with open(self._file, 'w') as f:
            json.dump(self._json, f)

    def update_model_info(self, info: ModelInfo):
        self._json['info'] = info
        self._update()

    def get_duo_words(self, filter: str='', unassigned_only: bool=False) -> List[str]:
        start_matches = sorted([duo_word for duo_word, anki_key in self._json['duo'].items() if (duo_word.lower().startswith(filter.lower())) and (unassigned_only == False or self._json['duo'][duo_word] not in self._json['anki'])])
        other_matches = sorted([duo_word for duo_word, anki_key in self._json['duo'].items() if (filter.lower() in duo_word.lower()) and (unassigned_only == False or self._json['duo'][duo_word] not in self._json['anki']) and (duo_word not in start_matches)])        
        return start_matches + other_matches

    def get_duo_words_from_anki_key(self, anki_key: str) -> List[str]:
        return sorted([duo_word for duo_word, _anki_key in self._json['duo'].items() if anki_key == _anki_key])

    def get_duo_words_from_anki_word(self, anki_word: str):
        return self.get_duo_words_from_anki_key(self.get_anki_key_from_anki_word(anki_word))

    def update_duo_new_words_from_file(self, file: str):
        '''Updates the model JSON file with newly learned Duolingo words.'''
        with open(file, 'r') as f:
            self._update_duo_new_words(json.load(f))        

    def update_duo_new_words_from_str(self, duo_str: str):
        self._update_duo_new_words(json.loads(duo_str))

    def _update_duo_new_words(self, duo_json: dict):
        for _word in duo_json['vocab_overview']:
            word = _word['word_string']
            if word not in self._json['duo']:
                self._json['duo'].update({word: None})
        self._update()

    def delete_duo_word(self, duo_word: str):
        try:
            self._json['duo'].pop(duo_word)
        except KeyError:
            raise Model.ModelError('Duo key not in dict!')
        self._update()

    def link_duo_word_to_anki_word(self, duo_word: str, anki_word: str):
        anki_key = self.get_anki_key_from_anki_word(anki_word)
        self._json['duo'].update({duo_word: anki_key})
        self._update()

    def unlink_duo_word(self, duo_word: str):
        self._json['duo'][duo_word] = None
        self._update()

    def get_anki_words(self, filter: str='', no_translation_only: bool = False) -> List[str]:
        start_matches = sorted([anki_word for anki_word, translation in self._json['anki'].values() if (anki_word.lower().startswith(filter.lower())) and (no_translation_only == False or translation == '')])
        other_matches = sorted([anki_word for anki_word, translation in self._json['anki'].values() if (filter.lower() in anki_word.lower()) and (no_translation_only == False or translation=='') and (anki_word not in start_matches)])
        return start_matches + other_matches

    def get_anki_key_from_duo_word(self, duo_word: str) -> Optional[str]:
        try:
            return self._json['duo'][duo_word]
        except KeyError:
            raise Model.ModelError(f"Duo word {duo_word} doesn't exist")

    def get_anki_key_from_anki_word(self, anki_word: str) -> str:
        keys = [key for key in self._json['anki'] if self._json['anki'][key][0] == anki_word]

        if not len(keys):
            self.update_anki_entry(str(uuid.uuid4()), anki_word, '')
            return self.get_anki_key_from_anki_word(anki_word)
        key, = keys # should only be one
        return key

    def get_anki_entry(self, anki_key) -> Tuple[str, str]:
        try:
            return self._json['anki'][anki_key]
        except KeyError:
            raise Model.ModelError(f"Key {anki_key} doesn't exist!")

    def update_anki_entry(self, anki_key: str, anki_word: str, translation: str):
        self._json['anki'].update({anki_key: (anki_word, translation)})
        self._update()

    def delete_anki_entry(self, anki_key: str):
        try:
            self._json['anki'].pop(anki_key)
            for duo_word, key in self._json['duo'].items():
                if key == anki_key:
                    self.unlink_duo_word(duo_word)
        except KeyError:
            raise Model.ModelError(f"Anki key {anki_key} doesn't exist!")
        self._update()

    def export_anki_csv(self, file_out):
        with open(file_out, 'w') as f:
            f.write('\n'.join([f"{word};{trans}" for id, (word, trans) in self._json['anki'].items()]))

