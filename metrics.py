# Metrics.py
import ast
import re
import os
from collections import Counter
from math import log, log2

python_dp = (
    'if', 'elif', # Conditionals
    'for', 'while',  # Loops
    'except', 'finally',  # Try-except blocks
    'and', 'or'  # Logical operators
)


def count_lines_of_code(filename):
    lines_of_code = 0
    with open(filename, 'r') as file:
        for line in file:
            # Strip whitespace and check if line is not a comment or blank
            stripped_line = line.strip()
            if stripped_line and not stripped_line.startswith('#'):
                lines_of_code += 1
    return lines_of_code


def cyclomatic_complexity_with_reuse(filename):
    with open(filename, 'r') as file:
        file_content = file.read()

    # Abstract Syntax Tree
    tree = ast.parse(file_content)
    function_calls = get_function_calls(tree)
    functions_declared = get_function_declarations(tree)

    decision_points = 0
    for line in file_content.splitlines():
        stripped_line = line.strip()
        if stripped_line.startswith('if __name__ == "__main__"'):
            continue
        if any(stripped_line.startswith(dp) for dp in python_dp):
            decision_points += 1
            decision_points += stripped_line.count(' and ') + stripped_line.count(' or ')

    # Cyclomatic complexity as total decision points plus one
    complexity = decision_points + 1

    # Internal reuse using graph-based formula
    edges = len(function_calls)
    nodes = len(functions_declared)
    internal_reuse = edges - nodes + 1

    return complexity, internal_reuse

def get_function_calls(tree):
    function_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            function_calls.append(node.func.id)
    return function_calls

def get_function_declarations(tree):
    function_declarations = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_declarations.append(node.name)
    return function_declarations

# Remove comments and strings
def clean_code(code):
    code = re.sub(r"#.*", "", code)
    code = re.sub(r"'''(.*?)'''", "", code, flags=re.DOTALL)
    code = re.sub(r'"""(.*?)"""', "", code, flags=re.DOTALL)  
    # Remove all strings
    code = re.sub(r"\'(.*?)\'", "", code)
    code = re.sub(r'\"(.*?)\"', "", code)
    return code

def extract_tokens(code):
    code = clean_code(code)
    # Regex for Python operators
    operators_pattern = r'[\+\-\*/%=<>&|^~:,\(\)\[\]\{\}]'
    # Regex for Python operands
    operands_pattern = r'\b[A-Za-z_][A-Za-z0-9_]*\b|\b\d+\.?\d*\b'
    
    operators = re.findall(operators_pattern, code)
    operands = re.findall(operands_pattern, code)

    keywords = {"and", "or", "not", "is", "in", "del", "pass", "break", "continue", "return", "yield", "raise",
                "import", "from", "as", "class", "def", "with", "try", "except", "finally", "while", "for",
                "if", "elif", "else", "assert", "global", "nonlocal", "lambda", "True", "False", "None"}
    filtered_operands = [idn for idn in operands if idn not in keywords]
    operators.extend([op for op in operands if op in keywords])

    return operators, filtered_operands


def halstead_measure(filename):
    with open(filename, 'r') as file:
        code = file.read()

    operators, operands = extract_tokens(code)

    #print(f"operators: {operators}, \noperands: {operands}")

    # Count occurrences
    operators_count = Counter(operators)
    operands_count = Counter(operands)
    
    # Calculate Halstead measures
    n1 = len(operators_count)  # unique operators
    n2 = len(operands_count)  # unique operands
    N1 = sum(operators_count.values())  # total operators
    N2 = sum(operands_count.values())  # total operands
    
    n = n1 + n2
    N = N1 + N2
    
    return N, n


def halstead_volume(N, n):
    volume = N * log2(n)
    return volume
    

# Maintainability Index = MAX(0,(171 - 5.2 * ln(Halstead Volume) - 0.23 * (Cyclomatic Complexity) - 16.2 * ln(Lines of Code))*100 / 171)
def maintainability_index(vol, comp, loc):
    maint_index = max(0,(171 - 5.2 * log(vol) - 0.23 * (comp) - 16.2 * log(loc))*100 / 171)
    if(maint_index > 19):
        flag = "Index is 20-100. Code is acceptable and 'easily' maintanable."
    elif(maint_index > 9 and maint_index < 20):
        flag = 'Index is 10-19. Code could benefit from refactoring.'
    elif(maint_index < 10):
        flag = 'Index < 10. Code is hard to maintain and problematic.'
    return maint_index, flag
