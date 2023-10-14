def handle_negation(formula):
    """Check if formula starts with the negation symbol and handle it."""
    negation = ['¬', '~']
    return formula[0] in negation and is_well_formed(formula[1:])


def find_operator_position(formula):
    """Find the position of the '*' operator at the top level."""
    count, index = 0, -1
    for i, char in enumerate(formula):
        if char == '(':
            count += 1
        elif char == ')':
            count -= 1
        elif char in ["∧", "∨", "≡", "⊃", "&", "*"] and count == 1:
            index = i
            return i
    return index


def has_disallowed_chars(formula):
    """Check if formula contains any of the disallowed characters."""
    for char in ['(', ')', '*']:
        if char in formula: return True
    return False


def is_well_formed(formula):
    """Check if a formula is well-formed recursively."""
    # Base cases
    if not formula: return False

    # Handle negation
    if handle_negation(formula): return True

    # Check for balanced parentheses and presence of the '*' operator
    if formula[0] == '(' and formula[-1] == ')':
        operator_position = find_operator_position(formula)
        return operator_position > 0 and is_well_formed(formula[1:operator_position]) and is_well_formed(
            formula[operator_position + 1:-1])

    # Check for any disallowed characters in the formula
    return not has_disallowed_chars(formula)


def is_wff(formula):
    list_op = ["∧", "∨", "≡", "⊃", "&"]
    for op in list_op: formula = formula.replace(op, "*")
    formula = formula.replace(" ", "")
    return is_well_formed(formula)


class Node:
    def __init__(self, value):
        self.value = value
        self.children = []


def get_tree(formula):

    list_op = ["∧", "∨", "≡", "⊃"]
    if formula[0] == '¬':
        node = Node('¬')
        node.children.append(get_tree(formula[1:]))
        return node
    else:
        count = 1
        index = -1
        for i in range(1, len(formula) - 1):
            if formula[i] in list_op and count == 1:
                index = i
                break
            elif formula[i] == '(':
                count += 1
            elif formula[i] == ')':
                count -= 1
        # print(index)
        if index >= 0:
            node = Node(formula[index])
            node.children.append(get_tree(formula[1:index]))
            node.children.append(get_tree(formula[index + 1:-1]))
        else:
            node = Node(formula)
            print(formula)
        return node

# Teste inicial
test_formula = "((P ∨ (R ∧ ¬S)) ∨ ¬(Q ∧ ¬P))"
result = get_tree(test_formula)
print(result)
