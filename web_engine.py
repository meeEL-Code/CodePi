import re

def parse_and_build(codepi_code):
    css_styles = {
        "body": ["font-family: Arial, sans-serif", "padding: 20px", "text-align: center"]
    }
    html_elements = []

    lines = codepi_code.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        # Background Color
        if line.startswith("make background color"):
            color = line.replace("make background color", "").strip()
            css_styles["body"].append(f"background-color: {color}")

        # Heading Creation
        elif line.startswith("create heading"):
            match = re.search(r'"([^"]*)"', line)
            if match:
                text = match.group(1)
                html_elements.append(f"  <h1 class='cp-heading'>{text}</h1>")

        # Heading Styling
        elif line.startswith("make heading color"):
            color = line.replace("make heading color", "").strip()
            if ".cp-heading" not in css_styles:
                css_styles[".cp-heading"] = []
            css_styles[".cp-heading"].append(f"color: {color}")

        # Button Creation
        elif line.startswith("create button"):
            match = re.search(r'"([^"]*)"', line)
            if match:
                text = match.group(1)
                html_elements.append(f"  <button class='cp-btn'>{text}</button>")

        # Button Styling
        elif line.startswith("make button color"):
            color = line.replace("make button color", "").strip()
            if ".cp-btn" not in css_styles:
                css_styles[".cp-btn"] = ["padding: 12px 24px", "border: none", "border-radius: 8px", "cursor: pointer"]
            css_styles[".cp-btn"].append(f"background-color: {color}")

    # Generate CSS block
    css_output = "<style>\n"
    for selector, rules in css_styles.items():
        css_output += f"{selector} {{\n  " + ";\n  ".join(rules) + ";\n}\n"
    css_output += "</style>"

    # Generate Full HTML
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CodePi Web Output</title>
    {css_output}
</head>
<body>
{chr(10).join(html_elements)}
</body>
</html>"""

    return full_html

# Sample CodePi Script
codepi_script = """
# CodePi Web Example
make background color #121212
create heading "Welcome to CodePi"
make heading color #ffffff
create button "Get Started"
make button color #007bff
"""

# Output to index.html
compiled_html = parse_and_build(codepi_script)
with open("index.html", "w") as f:
    f.write(compiled_html)

print("[SUCCESS] CodePi script compiled to index.html successfully!")
