def parser(tokens):
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
