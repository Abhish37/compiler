source_code = """
ABH 3
ABH 5
"""

tokens = lexer(source_code)
parsed = parser(tokens)
semantic_analysis(parsed)
code_generator(parsed)
