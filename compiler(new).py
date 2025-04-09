import os

# === AST Node Definitions ===
class ASTNode: pass

class Assignment(ASTNode):
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

class BinaryOp(ASTNode):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class Variable(ASTNode):
    def __init__(self, name):
        self.name = name

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

class IfElse(ASTNode):
    def __init__(self, condition, if_block, else_block):
        self.condition = condition
        self.if_block = if_block
        self.else_block = else_block

class While(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

# === Instruction Generator ===
class InstructionGenerator:
    def __init__(self):
        self.instructions = []
        self.register_count = 1
        self.label_count = 1
        self.variables = {}

    def get_register(self):
        reg = f"R{self.register_count}"
        self.register_count += 1
        return reg

    def get_label(self):
        label = f"L{self.label_count}"
        self.label_count += 1
        return label

    def generate(self, ast_nodes):
        for node in ast_nodes:
            self.generate_node(node)
        return self.instructions

    def generate_node(self, node):
        if isinstance(node, Assignment):
            reg = self.evaluate_expr(node.expr)
            self.instructions.append(f"MORP {node.var}, {reg}")
            self.variables[node.var] = reg

        elif isinstance(node, IfElse):
            label_true = self.get_label()
            label_end = self.get_label()
            cond_reg = self.evaluate_expr(node.condition)
            self.instructions.append(f"SNIF {cond_reg} GOTO {label_true}")
            for stmt in node.else_block:
                self.generate_node(stmt)
            self.instructions.append(f"ZUG {label_end}")
            self.instructions.append(f"KRONK {label_true}:")
            for stmt in node.if_block:
                self.generate_node(stmt)
            self.instructions.append(f"KRONK {label_end}:")

        elif isinstance(node, While):
            label_start = self.get_label()
            label_end = self.get_label()
            self.instructions.append(f"KRONK {label_start}:")
            cond_reg = self.evaluate_expr(node.condition)
            self.instructions.append(f"SNARF {cond_reg} GOTO {label_end}")
            for stmt in node.body:
                self.generate_node(stmt)
            self.instructions.append(f"ZUG {label_start}")
            self.instructions.append(f"KRONK {label_end}:")

    def evaluate_expr(self, expr):
        if isinstance(expr, Number):
            reg = self.get_register()
            self.instructions.append(f"ZARG {reg}, {expr.value}")
            return reg
        elif isinstance(expr, Variable):
            return self.variables.get(expr.name, f"${expr.name}")
        elif isinstance(expr, BinaryOp):
            left = self.evaluate_expr(expr.left)
            right = self.evaluate_expr(expr.right)
            reg = self.get_register()
            op_map = {
                '+': 'BLOT',
                '-': 'FRIK',
                '*': 'TRUK',
                '/': 'QUOX',
                '**': 'PLAX'
            }
            op_instr = op_map.get(expr.op, 'BLOT')
            self.instructions.append(f"{op_instr} {reg}, {left}, {right}")
            return reg

# === Simple Tokenizer and Parser ===
def tokenize(code):
    lines = code.strip().split('\n')
    return [line.rstrip() for line in lines if line.strip()]

def parse_expression(expr):
    expr = expr.strip()
    for op in ['**', '+', '-', '*', '/']:
        if op in expr:
            parts = expr.split(op)
            if len(parts) == 2:
                left, right = map(str.strip, parts)
                return BinaryOp(op, parse_expression(left), parse_expression(right))
    if expr.isdigit():
        return Number(expr)
    return Variable(expr)

def parse(lines):
    i = 0
    ast = []

    def parse_block(start):
        block = []
        nonlocal i
        while i < len(lines) and (lines[i].startswith("    ") or lines[i].startswith("\t")):
            block.append(lines[i].strip())
            i += 1
        return parse(block)

    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("if "):
            condition = line[3:-1].strip()
            i += 1
            if_block = parse_block(i)
            else_block = []
            if i < len(lines) and lines[i].strip() == "else:":
                i += 1
                else_block = parse_block(i)
            ast.append(IfElse(parse_expression(condition), if_block, else_block))
        elif line.startswith("while "):
            condition = line[6:-1].strip()
            i += 1
            body = parse_block(i)
            ast.append(While(parse_expression(condition), body))
        elif "=" in line:
            var, expr = map(str.strip, line.split('='))
            ast.append(Assignment(var, parse_expression(expr)))
            i += 1
        else:
            i += 1
    return ast

# === Driver ===
if __name__ == "__main__":
    with open("input.txt", "r") as f:
        code = f.read()

    lines = tokenize(code)
    ast_nodes = parse(lines)

    generator = InstructionGenerator()
    instructions = generator.generate(ast_nodes)

    with open("output.txt", "w") as f:
        for instr in instructions:
            f.write(instr + "\n")

    print("Custom instructions written to:", os.path.abspath("output.txt"))
