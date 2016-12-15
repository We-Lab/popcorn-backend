import random
import re

from mysite.settings import BAD_WORDS


class ProfanitiesFilter(object):
    def __init__(self, ignore_case=True, replacements='$@%-?!', inside_words=True):
        """
        :param filterlist: 금지 단어
        :param ignore_case: 대소문자 무시
        :param replacements: 대체 단어
        :param inside_words: 양옆 공백 포함여부
        """
        self.bad_words = BAD_WORDS['bad_words']
        self.ignore_case = ignore_case
        self.replacements = replacements
        self.inside_words = inside_words

    def _make_clean_word(self, length):
        # length 만큼 대체 문자 출력
        return ''.join([random.choice(self.replacements) for i in range(length)])

    def __replacer(self, match):
        value = match.group()
        return self._make_clean_word(len(value))

    def clean(self, text):
        regexp_inside_words = {
            True: r'(%s)',
            False: r'\b(%s)\b',
        }
        # (a|b)g => ag, bg
        regexp = (regexp_inside_words[self.inside_words] % '|'.join(self.bad_words))
        r = re.compile(regexp, re.IGNORECASE if self.ignore_case else 0)
        # re.sub 사용법 https://docs.python.org/2/library/re.html#re.sub
        return r.sub(self.__replacer, text)
