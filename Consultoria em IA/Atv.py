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
    # Se a formula for atômica, retorne um nó com essa formula

    formula = formula.replace(" ", "")

    if is_wff(formula) and len(formula) == 1:
        return Node(formula)

    # Se a formula começa com uma negação, crie um nó para a negação e um nó filho para o resto da formula
    if formula[0] in ['¬', '~']:
        node = Node(formula[0])
        node.children.append(get_tree(formula[1:]))
        return node

    # Encontre a posição do conectivo principal
    operator_position = find_operator_position(formula)

    # Crie um nó para o conectivo principal
    node = Node(formula[operator_position])

    # Divida a formula em subfórmulas e chame a função recursivamente para cada uma
    left_subformula = formula[1:operator_position]
    right_subformula = formula[operator_position + 1:-1]

    node.children.append(get_tree(left_subformula))
    node.children.append(get_tree(right_subformula))

    return node


# Teste inicial
test_formula = "((P ∨ (R ∧ ¬S)) ∨ ¬(Q ∧ ¬P))"
result = get_tree(test_formula)
print(result)
