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

# Separate by function
def cyclomatic_complexity(filename):
    decision_points = 0
    with open(filename, 'r') as file:
        for line in file:
            stripped_line = line.strip()
            if stripped_line.startswith('if __name__ == "__main__"'):
                continue
            if any(stripped_line.startswith(dp) for dp in python_dp):
                decision_points += 1
                decision_points += stripped_line.count(' and ') + stripped_line.count(' or ')
    return decision_points + 1
