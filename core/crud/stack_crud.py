from typing import List, Optional

from core.models import Stack


class StackCRUD:
    def __init__(self):
        self.stacks: List[Stack] = []

    def get(self, _id) -> Optional[Stack]:
        for stack in self.stacks:
            if str(stack.id) == _id:
                return stack
        return None

    def create(self, stack: Stack = None, content: List[str] = None) -> Stack:
        if stack is None:
            stack = Stack(content)
        self.stacks.append(stack)
        return stack

    def update(self, stack_id, stack: Stack = None) -> Optional[Stack]:
        stack_found = self.get(stack_id)
        if stack_found is None:
            return None

        stack_found.update(content=stack.content, operand=stack.operand)
        return stack_found

    def delete(self, stack_id):
        stack = self.get(stack_id)
        self.stacks.remove(stack)
