import re

# CodePi Lexer & Interpreter Engine
def run_codepi(code):
    print("=== CodePi Engine Output ===")
    variables = {}
    lines = code.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        # Example: set x to 10
        if line.startswith('set '):
            parts = line.split()
            var_name = parts[1]
            val = parts[3]
            variables[var_name] = int(val) if val.isdigit() else val.strip('"')
        
        # Example: add 5 to x
        elif line.startswith('add '):
            parts = line.split()
            num = int(parts[1])
            var_name = parts[3]
            if var_name in variables:
                variables[var_name] += num

        # Example: say "Hello" or show x
        elif line.startswith('say ') or line.startswith('show '):
            content = line.split(' ', 1)[1]
            if content.startswith('"') and content.endswith('"'):
                print(content.strip('"'))
            elif content in variables:
                print(variables[content])
            else:
                print(content)

# Test Script
sample_script = """
# CodePi Test Script
set score to 10
add 5 to score
say "Final Score:"
show score
"""

if __name__ == "__main__":
    run_codepi(sample_script)
