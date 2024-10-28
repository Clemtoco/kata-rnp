from typing import List


def evaluate_rpn(stack_content: List[str]):
    stack = []

    for token in stack_content:
        if token.lstrip("+").isdigit() or token.lstrip("-").isdigit():
            stack.append(int(token))
            continue

        last = stack.pop()
        next_last = stack.pop()

        if token == "+":
            stack.append(next_last + last)
        elif token == "-":
            stack.append(next_last - last)
        elif token == "*":
            stack.append(next_last * last)
        elif token == "/":
            try:
                stack.append(int(next_last / last))
            except ZeroDivisionError:
                raise ValueError(f"Cannot divide by zero: {next_last} / {last}")
        else:
            stack.append(next_last)
            stack.append(last)

    return stack
