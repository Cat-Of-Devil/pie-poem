import pymorphy2
import json

# http://textmechanic.com/text-tools/basic-text-tools/remove-duplicate-lines/
# http://www.codeisart.ru/blog/python-shingles-algorithm/
def canonize_words(words: list) -> list:
    stop_words = ('быть', 'мой', 'наш', 'ваш', 'их', 'его', 'её', 'их',
                  'этот', 'тот', 'где', 'который', 'либо', 'нибудь', 'нет', 'да')
    grammars = {'NOUN': '_S',
                'VERB': '_V', 'INFN': '_V', 'GRND': '_V', 'PRTF': '_V', 'PRTS': '_V',
                'ADJF': '_A', 'ADJS': '_A',
                'ADVB': '_ADV',
                'PRED': '_PRAEDIC'}

    morph = pymorphy2.MorphAnalyzer()
    normalized = []
    for i in words:
        forms = morph.parse(i)
        try:
            form = max(forms, key=lambda x: (x.score, x.methods_stack[0][2]))
        except Exception:
            form = forms[0]
            print(form)
        if not (form.tag.POS in ['PREP', 'CONJ', 'PRCL', 'NPRO', 'NUMR']
                or 'Name' in form.tag
                or 'UNKN' in form.tag
                or form.normal_form in stop_words):  # 'ADJF'
            normalized.append(form.normal_form + grammars.get(form.tag.POS, ''))
    return normalized


def read_data_model(file_name: str) -> dict:
    file = open(file_name, mode='r', encoding='utf-8')
    return json.load(file)


def write_data_model(file_name: str, data_model: dict):
    file = open(file_name, mode='w', encoding='utf-8')
    json.dump(data_model, file, separators=(',', ':'), ensure_ascii=False)