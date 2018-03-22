from typing import Dict

from insightepy.errors import InvalidParameterException


class Extractor(object):
    def _validate_params(self) -> None:
        pass

    def to_dict(self) -> Dict:
        pass


class NGram(Extractor):
    _label_ = 'NGram'

    def __init__(self, name='ngram', n=3):
        self.name = name
        self.n = n
        self._validate_params()

    def _validate_params(self):
        if not isinstance(self.n, int):
            raise InvalidParameterException('n need to be of type integer')

    def to_dict(self):
        return dict(
            label=self._label_,
            name=self.name,
            n=self.n
        )
