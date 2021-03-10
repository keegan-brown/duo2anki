from duo2anki.model import Model

# debug
m = Model('test')
m.update_duo_words('res/test.json')
m.assign_duo_word('boek', 'het boek')