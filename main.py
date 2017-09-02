import json

from PIL import Image, ImageDraw, ImageFont
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

    print(actual)

    return actual == correct

def draw_haiku(haiku):
    im = Image.new("RGBA", (400, 400), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype("~/fonts/Hack/Hack-Regular.ttf", 35)
    text_size = dr.textsize(haiku, font)
    dr.text(
        ((im.size[0] - text_size[0]) / 2, (im.size[1] - text_size[1]) / 2),
        haiku, (0, 0, 0), font=font
    )
    im.show()


if __name__ == '__main__':
    draw_haiku("Hello World!\nHello World!\nHelloWorld!")
