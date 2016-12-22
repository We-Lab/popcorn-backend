""" 욕설필터 module

욕설을 특수문자로 변경해서 저장합니다.

"""
import random
import re

from mysite.settings import BAD_WORDS


class ProfanitiesFilter(object):
    """
    1. 욕설 필터링
    2. 욕설 list는 django-config/bad_words.json 파일에서 관리함
    """
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
        """
        length 만큼 대체 문자 출력

        :param length: 단어길이
        :return: 특수문자화 된 단어
        """
        return ''.join([random.choice(self.replacements) for i in range(length)])

    def __replacer(self, match):
        """
        일치하는 regex 객체를 받아서 text로 변경하고 길이만큼 랜덤특수문자 출력

        :param match: 일치하는 regex 객체
        :return: 변경된 텍스트
        """
        value = match.group()
        return self._make_clean_word(len(value))

    def clean(self, text):
        """
        1. inside_words, ignore_case 값을 확인하고 regex compile
        2. 패턴과 일치하는 횟수만큼 __replacer 호출하여 텍스트 변경

        :param text: 입력 텍스트
        :return: 변환된 텍스트
        """
        regexp_inside_words = {
            True: r'(%s)',
            False: r'\b(%s)\b',
        }
        regexp = (regexp_inside_words[self.inside_words] % '|'.join(self.bad_words))
        r = re.compile(regexp, re.IGNORECASE if self.ignore_case else 0)
        return r.sub(self.__replacer, text)
