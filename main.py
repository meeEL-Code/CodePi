import sys
import re

def compile_cp(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    css_rules = {
        "body": ["font-family: sans-serif", "padding: 50px", "text-align: center", "transition: all 0.4s ease"]
    }
    html_elements = []
    js_events = []
    
    in_when_block = False
    current_target = None

    for line in lines:
        raw_line = line
        line_str = line.strip()
        
        if not line_str or line_str.startswith('#'):
            continue

        # Handle 'when' block and indentation
        if line_str.startswith('when ') and line_str.endswith(':'):
            in_when_block = True
            match = re.search(r'"([^"]*)"', line_str)
            if match:
                current_target = match.group(1)
            continue

        if in_when_block:
            if raw_line.startswith('    ') or raw_line.startswith('\t'):
                if "make background color" in line_str:
                    color = line_str.replace("make background color", "").strip()
                    js_events.append(f'document.body.style.backgroundColor = "{color}";')
                elif "say " in line_str:
                    msg = line_str.replace("say ", "").strip().strip('"')
                    js_events.append(f'alert("{msg}");')
                continue
            else:
                in_when_block = False

        # Background
        if line_str.startswith("make background color"):
            color = line_str.replace("make background color", "").strip()
            css_rules["body"].append(f"background-color: {color}")

        # Heading
        elif line_str.startswith("create heading"):
            match_text = re.search(r'"([^"]*)"', line_str)
            match_id = re.search(r'with name "([^"]*)"', line_str)
            text = match_text.group(1) if match_text else "Heading"
            elem_id = match_id.group(1) if match_id else "heading1"
            html_elements.append(f'  <h1 id="{elem_id}">{text}</h1>')

        # Button
        elif line_str.startswith("create button"):
            match_text = re.search(r'"([^"]*)"', line_str)
            match_id = re.search(r'with name "([^"]*)"', line_str)
            text = match_text.group(1) if match_text else "Button"
            elem_id = match_id.group(1) if match_id else "btn1"
            html_elements.append(f'  <button id="{elem_id}" class="cp-btn">{text}</button>')

        # Styling
        elif line_str.startswith("make "):
            match_id = re.search(r'"([^"]*)"', line_str)
            if match_id:
                elem_id = match_id.group(1)
                if "color" in line_str:
                    color = line_str.split("color")[-1].strip()
                    selector = f"#{elem_id}"
                    if selector not in css_rules:
                        css_rules[selector] = []
                    css_rules[selector].append(f"color: {color}")

    # General Button CSS Styling
    if ".cp-btn" not in css_rules:
        css_rules[".cp-btn"] = ["padding: 14px 28px", "font-size: 16px", "border: none", "border-radius: 8px", "cursor: pointer", "font-weight: bold"]

    # Generate CSS string
    css_out = "<style>\n"
    for sel, rules in css_rules.items():
        css_out += f"{sel} {{\n  " + ";\n  ".join(rules) + ";\n}\n"
    css_out += "</style>"

    # Generate JS string
    js_code_block = "\n    ".join(js_events)
    js_out = f"""<script>
document.addEventListener('DOMContentLoaded', () => {{
  const targetBtn = document.getElementById("{current_target}");
  if(targetBtn) {{
    targetBtn.addEventListener("click", () => {{
      {js_code_block}
    }});
  }}
}});
</script>""" if current_target else ""

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CodePi App</title>
    {css_out}
</head>
<body>
{chr(10).join(html_elements)}

{js_out}
</body>
</html>"""

    with open("index.html", "w") as f:
        f.write(full_html)
    print(f"[SUCCESS] Compiled '{filename}' successfully to 'index.html'!")

if __name__ == "__main__":
    target_file = sys.argv[1] if len(sys.argv) > 1 else "app.cp"
    compile_cp(target_file)
