import aspell
import itertools
import unicodedata
from typing.re import Match


class Speller(object):
    def __init__(self, language: str) -> None:
        self.language = language
        self.s = aspell.Speller('lang', language)

    def __try_fix(self, word: str) -> str:
        if self.s.check(word):
            return word
        suggestions = self.s.suggest(word)
        if len(suggestions) > 0:
            return suggestions[0]
        return word

    @staticmethod
    def __is_letter(c: str) -> bool:
        return unicodedata.category(c)[0] == 'L'

    def fix(self, sentence: str) -> str:
        parts = []
        for k, g in itertools.groupby(sentence, key=Speller.__is_letter):
            part = ''.join(g)
            if k == 'L':
                part = self.__try_fix(part)
            parts.append(part)
        return ''.join(parts)
