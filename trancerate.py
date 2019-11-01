from urllib.parse import quote

from selenium import webdriver
import pyperclip

import chromedriver_binary


class Reader:
    def read_input(self):
        s = ''
        a = input()
        while a != '':
            s += '\n' + a
            a = input()

        return s

    def parse_article(self, art: str):
        import re
        section_re = re.compile(r'^[0-9]+(\.[0-9]+)*$')
        s = ''
        h = ''
        ret = []
        for formula in art.splitlines(True):
            orig = formula
            strip = formula.strip('\n')
            split = formula.split(' ', maxsplit=1)
            if section_re.match(split[0].strip()):
                h = strip
            elif strip and strip[-1] in '.:;)':
                s += orig + '\n'
                ret.append((h, s))
                h = ''
                s = ''
            elif strip and strip[0] in '・-•—':
                ret.append((h, s))
                s = strip + ' '
                h = ''
            else:
                s += strip + ' '
        if s:
            ret.append((h, s))
        return ret

    def get_article(self):
        return self.parse_article(self.read_input())


class Translator:
    url = 'https://translate.google.com/?hl=ja#view=home&op=translate&sl=en&tl=ja&text='

    def __init__(self):
        self.driver = webdriver.Chrome()

    def open(self, s):
        s = quote(s)
        url = self.url + s
        self.driver.get(url)
        import time
        time.sleep(2)

    def copy(self):
        button = self.driver.find_element_by_class_name('tlid-copy-translation-button')
        button.click()
        import time
        time.sleep(1)
        return pyperclip.paste()


class Writer:
    filename: str

    def __init__(self, filename):
        self.filename = filename

    def write_append(self, t):
        if not t:
            return
        with open(self.filename, 'a') as file:
            file.write(t + '\n\n')


if __name__ == '__main__':
    import sys
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = 'translate.txt'

    reader = Reader()
    translator = Translator()
    writer = Writer(file_name)
    import re
    num_re = re.compile('[0-9]+')

    while True:
        a = reader.get_article()
        for h, t in a:
            if h:
                n = len(num_re.findall(h.split(' ', maxsplit=1)[0]))
                h = '#' * (n + 1) + ' ' + h
                writer.write_append(h)
            translator.open(t)
            b = translator.copy()
            writer.write_append(b)
