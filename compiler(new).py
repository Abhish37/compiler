import os

class InstructionGenerator:
    def __init__(self):
        self.instructions = []
        self.register_count = 1
        self.label_count = 1
        self.variables = {}
        self.lines = []

    def get_register(self):
        reg = f"R{self.register_count}"
        self.register_count += 1
        return reg

    def get_label(self):
        label = f"L{self.label_count}"
        self.label_count += 1
        return label

    def tokenize(self, code):
        return [line.rstrip() for line in code.strip().split('\n') if line.strip()]

    def is_indented(self, line):
        return line.startswith("    ") or line.startswith("\t")

    def evaluate_expr(self, expr):
        expr = expr.strip()
        for op in ['**', '+', '-', '*', '/']:
            if op in expr:
                left, right = map(str.strip, expr.split(op))
                r1 = self.evaluate_expr(left)
                r2 = self.evaluate_expr(right)
                r3 = self.get_register()
                op_map = {
                    '+': 'BLOT',
                    '-': 'FRIK',
                    '*': 'TRUK',
                    '/': 'QUOX',
                    '**': 'PLAX'
                }
                instr = op_map.get(op, 'BLOT')
                self.instructions.append(f"{instr} {r3}, {r1}, {r2}")
                return r3
        if expr.isdigit():
            r = self.get_register()
            self.instructions.append(f"ZARG {r}, {expr}")
            return r
        if expr in self.variables:
            return self.variables[expr]
        else:
            r = self.get_register()
            self.instructions.append(f"ZARG {r}, {expr}")
            self.variables[expr] = r
            return r

    def handle_assignment(self, line):
        var, expr = map(str.strip, line.split('='))
        reg = self.evaluate_expr(expr)
        self.instructions.append(f"MORP {var}, {reg}")
        self.variables[var] = reg

    def handle_if_else(self, i):
        condition = self.lines[i][3:-1].strip()
        label_true = self.get_label()
        label_end = self.get_label()

        cond_reg = self.evaluate_expr(condition)
        self.instructions.append(f"SNIF {cond_reg} GOTO {label_true}")

        i += 1
        while i < len(self.lines) and self.is_indented(self.lines[i]):
            self.handle_line(self.lines[i].strip())
            i += 1

        self.instructions.append(f"ZUG {label_end}")
        self.instructions.append(f"KRONK {label_true}:")

        if i < len(self.lines) and self.lines[i].strip() == "else:":
            i += 1
            while i < len(self.lines) and self.is_indented(self.lines[i]):
                self.handle_line(self.lines[i].strip())
                i += 1

        self.instructions.append(f"KRONK {label_end}:")
        return i

    def handle_while(self, i):
        condition = self.lines[i][6:-1].strip()
        label_start = self.get_label()
        label_end = self.get_label()

        self.instructions.append(f"KRONK {label_start}:")
        cond_reg = self.evaluate_expr(condition)
        self.instructions.append(f"SNARF {cond_reg} GOTO {label_end}")

        i += 1
        while i < len(self.lines) and self.is_indented(self.lines[i]):
            self.handle_line(self.lines[i].strip())
            i += 1

        self.instructions.append(f"ZUG {label_start}")
        self.instructions.append(f"KRONK {label_end}:")
        return i

    def handle_line(self, line):
        if line.startswith("if "):
            return self.handle_if_else(self.lines.index(line))
        elif line.startswith("while "):
            return self.handle_while(self.lines.index(line))
        elif "=" in line:
            self.handle_assignment(line)
        return self.lines.index(line) + 1

    def generate(self, code):
        self.lines = self.tokenize(code)
        i = 0
        while i < len(self.lines):
            line = self.lines[i].strip()
            if line == "":
                i += 1
                continue
            if line.startswith("if "):
                i = self.handle_if_else(i)
            elif line.startswith("while "):
                i = self.handle_while(i)
            else:
                self.handle_line(line)
                i += 1
        return self.instructions

# === Driver Code ===
if __name__ == "__main__":
    with open("input.txt", "r") as f:
        code = f.read()

    generator = InstructionGenerator()
    instructions = generator.generate(code)

    with open("output.txt", "w") as f:
        for instr in instructions:
            f.write(instr + "\n")

    print("Custom instructions written to:", os.path.abspath("output.txt"))