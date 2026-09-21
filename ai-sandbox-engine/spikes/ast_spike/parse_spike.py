import tree_sitter_python as tspython
from tree_sitter import Language, Parser

# 1. Tell tree-sitter which language to understand
PY_LANGUAGE = Language(tspython.language())
parser = Parser(PY_LANGUAGE)

# 2. Read the file as bytes (tree-sitter wants bytes, not text)
with open("sample_vuln.py", "rb") as f:
    source = f.read()

# 3. Parse it into a tree
tree = parser.parse(source)
root = tree.root_node

print("Root node type:", root.type)
print("Has syntax errors?", root.has_error)
print()
print("Raw tree:")
print(root)
print()

# 4. Print a readable, indented version of the tree
def print_tree(node, depth=0):
    indent = "  " * depth
    start_line = node.start_point[0] + 1   # +1 because tree-sitter counts lines from 0
    end_line = node.end_point[0] + 1
    extra = ""
    if node.child_count == 0:
        extra = " -> " + node.text.decode("utf8")
    print(f"{indent}{node.type} [line {start_line}-{end_line}]{extra}")
    for child in node.named_children:
        print_tree(child, depth + 1)

print("Readable tree:")
print_tree(root)