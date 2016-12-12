import aspell
import re
from typing.re import Match


class Speller(object):
    alphabets = {
        'en': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'pl': ('aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż'
               'AĄBCĆDEĘFGHIJKLŁMNŃOÓPQRSŚTUVWXYZŹŻ')
    }

    def __init__(self, language: str) -> None:
        if language not in Speller.alphabets:
            raise Exception('Unknown language')
        self.language = language
        self.s = aspell.Speller('lang', language)
        self.word_re = re.compile(
                '[{}]+'.format(Speller.alphabets[self.language]))

    def __try_replace(self, m: Match) -> str:
        word = m.group(0)
        if self.s.check(word):
            return word
        suggestions = self.s.suggest(word)
        if len(suggestions) > 0:
            return suggestions[0]
        return word

    def fix(self, sentence: str) -> str:
        return self.word_re.sub(self.__try_replace, sentence)
