def semantic_analysis(parsed_instructions):
    for instr in parsed_instructions:
        if instr['type'] == 'ABH':
            if instr['value'] < 0:
                raise ValueError("Exponent must be non-negative")
