
from typing import Protocol
from translate import Translator as Trans


class Translator(Protocol):
    def translate(self, city: str) -> str:
        raise NotImplementedError


class MyTranslator:

    def __init__(self, from_lang, to_lang):
        self._from = from_lang
        self._to = to_lang
        self._translator = Trans(from_lang=from_lang, to_lang=to_lang)

    def translate(self, city: str) -> str:
        translation = self._translator.translate(city)
        return translation
