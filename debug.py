from duo2anki.model import Model

# debug
m = Model('test')
m.update_duo_words('res/test.json')
m.assign_duo_word('boek', 'het boek')
m.assign_anki_translation('het boek', 'the book')