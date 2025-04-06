# main.py

def lexer(source_code):
    """Breaks input code into tokens."""
    tokens = []
    lines = source_code.strip().splitlines()
    for line in lines:
        parts = line.strip().split()
        if not parts:
            continue
        tokens.append({
            'instruction': parts[0],
            'argument': parts[1] if len(parts) > 1 else None
        })
    return tokens


def parser(tokens):
    """Converts tokens into structured instructions."""
    parsed = []
    for token in tokens:
        instr = token['instruction']
        arg = token['argument']
        if instr != "ABH":
            raise ValueError(f"Unsupported instruction: {instr}")
        if not arg or not arg.isdigit():
            raise ValueError(f"Invalid argument for ABH: {arg}")
        parsed.append({
            'type': 'ABH',
            'value': int(arg)
        })
    return parsed


def semantic_analysis(parsed_instructions):
    """Checks for logical correctness."""
    for instr in parsed_instructions:
        if instr['type'] == 'ABH':
            if instr['value'] < 0:
                raise ValueError("Exponent must be non-negative")


def code_generator(parsed_instructions):
    """Executes instructions and returns their evaluated results."""
    results = []
    for instr in parsed_instructions:
        if instr['type'] == 'ABH':
            n = instr['value']
            result = 3 ** n
            results.append({
                'instruction': f'ABH {n}',
                'result': result
            })
    return results


def main():
    # Simulate source code input
    source_code = """
    ABH 2
    ABH 4
    ABH 0
    """

    try:
        tokens = lexer(source_code)
        parsed = parser(tokens)
        semantic_analysis(parsed)
        evaluated = code_generator(parsed)

        # Print Evaluation Results
        print("=== Evaluation Results ===")
        for item in evaluated:
            print(f"{item['instruction']}  =>  {item['result']}")
    except ValueError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
