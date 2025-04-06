def lexer(source_code):
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
