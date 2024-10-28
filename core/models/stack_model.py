from typing import List, Optional
from uuid import uuid4

from core.utils import evaluate_rpn


class Stack:
    def __init__(self, operand=None, content=None, _id=None):
        self.id = uuid4() if _id is None else _id
        self._content: List[str] = content if content is not None else []
        self.operand: Optional[str] = operand

    @property
    def content(self):
        return evaluate_rpn(self._content)

    @content.setter
    def content(self, value: List[str]):
        self._content = value

    def __repr__(self):
        return "Stack {} has a content {}".format(self.id, self.content)

    def update(
        self, content: Optional[List[str]] = None, operand: Optional[str] = None
    ):

        if content is None and operand is None:
            return None

        if operand:
            self._content.append(operand)
        elif content is not None and len(content) > 0:
            self._content = content

        return self.content
