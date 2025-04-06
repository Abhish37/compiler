def code_generator(parsed_instructions):
    for instr in parsed_instructions:
        if instr['type'] == 'ABH':
            n = instr['value']
            result = 3 ** n
            print(f"3^{n} = {result}")
