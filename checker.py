import re

class Checker:
    def __init__(self):
        self.supported_functions = {
            "log10": None,  # Placeholder
            "sqrt": None    # Placeholder
        }

    def validate_function(self, func):
        """ Validate the function expression by inspecting for common issues. """
        func = func.replace(" ", "")  # Remove spaces for easier processing

        # Check for unsupported characters
        if not re.match(r'^[\d\w+\-*/().^log10sqrt]*$', func):
            return False, "Function contains unsupported characters."

        # Ensure that consecutive operators do not exist, excluding '**'
        if re.search(r'(?<!\*)[+\-*/]{2,}', func):  # Multiple operators in a row, excluding '**'
            return False, "Consecutive operators detected. Ensure that operators are correctly placed between operands."

        # Ensure that the function does not end with an operator
        if re.search(r'[+\-*/^]$', func):
            return False, "Function ends with an operator. Ensure that the function ends with a valid operand."

        # Ensure that the function does not start with an operator
        if re.search(r'^[+\-*/^]', func):
            return False, "Function starts with an operator. Ensure that the function starts with a valid operand."

        # Check for unmatched parentheses
        open_parens = 0
        for char in func:
            if char == '(':
                open_parens += 1
            elif char == ')':
                open_parens -= 1
            if open_parens < 0:
                return False, "Unmatched closing parenthesis. Ensure that all parentheses are properly opened."

        if open_parens > 0:
            return False, "Unmatched opening parenthesis. Ensure that all parentheses are properly closed."

        return True, ""

# Example usage:
checker = Checker()
result, message = checker.validate_function("sqrt(x)")
print(result, message)  # Expected output: True, ""
