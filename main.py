import json

from urllib.request import urlopen

BASE_URL = 'http://rhymebrain.com/talk?function=getWordInfo&word=%s'
_cache = {}


def get_word_info(word):
    if word in _cache:
        res = _cache[word]
    else:
        r = urlopen(BASE_URL % word)
        res = json.loads(r.read())
        _cache[word] = res

    return res


def get_syllables(word):
    word_info = get_word_info(word)
    return int(word_info['syllables'])


def get_line_syllables(sentence):
    words = sentence.split(" ")
    syllables = 0
    for word in words:
        syllables += get_syllables(word)

    return syllables


def is_haiku(haiku):
    sentences = haiku.split("\n")
    correct = [5, 7, 5]
    actual = []

    for sentence in sentences:
        actual.append(get_line_syllables(sentence))

    return actual == correct


if __name__ == '__main__':
    haiku = """Forget the sadness
    You will not be alone
    Honeydew melon
    """
    print(is_haiku(haiku))
