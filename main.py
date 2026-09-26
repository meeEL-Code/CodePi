import sys
import re
import os
import http.server
import socketserver

def compile_cp(filename):
    if not os.path.exists(filename):
        print(f"[ERROR] File '{filename}' not found!")
        return False

    with open(filename, 'r') as f:
        lines = f.readlines()

    css_rules = {
        "body": ["font-family: sans-serif", "padding: 50px", "text-align: center", "background-color: #121212", "color: white", "transition: all 0.4s ease"],
        "input": ["padding: 12px 18px", "font-size: 16px", "border-radius: 8px", "border: 1px solid #444", "margin: 10px", "background: #222", "color: #fff", "outline: none", "width: 80%"]
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
                elif "say text from" in line_str:
                    match_inp = re.search(r'"([^"]*)"', line_str)
                    if match_inp:
                        inp_id = match_inp.group(1)
                        js_events.append(f'const val = document.getElementById("{inp_id}").value; alert(val ? "Hello, " + val : "Please type something!");')
                elif "say " in line_str:
                    msg = line_str.replace("say ", "").strip().strip('"')
                    js_events.append(f'alert("{msg}");')
                continue
            else:
                in_when_block = False

        if line_str.startswith("make background color"):
            color = line_str.replace("make background color", "").strip()
            css_rules["body"].append(f"background-color: {color}")

        # New: Card Support
        elif line_str.startswith("start card"):
            match_id = re.search(r'"([^"]*)"', line_str)
            elem_id = match_id.group(1) if match_id else "card1"
            html_elements.append(f'  <div id="{elem_id}" class="cp-card">')

        elif line_str == "end card":
            html_elements.append('  </div>')

        elif line_str.startswith("create heading"):
            match_text = re.search(r'"([^"]*)"', line_str)
            match_id = re.search(r'with name "([^"]*)"', line_str)
            text = match_text.group(1) if match_text else "Heading"
            elem_id = match_id.group(1) if match_id else "heading1"
            html_elements.append(f'  <h2 id="{elem_id}">{text}</h2>')

        # New: Text Paragraph Support
        elif line_str.startswith("create text"):
            match_text = re.search(r'"([^"]*)"', line_str)
            match_id = re.search(r'with name "([^"]*)"', line_str)
            text = match_text.group(1) if match_text else "Text paragraph"
            elem_id = match_id.group(1) if match_id else "text1"
            html_elements.append(f'  <p id="{elem_id}" style="color: #ccc; line-height: 1.6;">{text}</p>')

        elif line_str.startswith("create input"):
            match_text = re.search(r'"([^"]*)"', line_str)
            match_id = re.search(r'with name "([^"]*)"', line_str)
            placeholder = match_text.group(1) if match_text else "Enter text..."
            elem_id = match_id.group(1) if match_id else "input1"
            html_elements.append(f'  <div><input type="text" id="{elem_id}" placeholder="{placeholder}"></div>')

        elif line_str.startswith("create button"):
            match_text = re.search(r'"([^"]*)"', line_str)
            match_id = re.search(r'with name "([^"]*)"', line_str)
            text = match_text.group(1) if match_text else "Button"
            elem_id = match_id.group(1) if match_id else "btn1"
            html_elements.append(f'  <div><button id="{elem_id}" class="cp-btn">{text}</button></div>')

        elif line_str.startswith("create image from"):
            match_src = re.search(r'from "([^"]*)"', line_str)
            match_id = re.search(r'with name "([^"]*)"', line_str)
            src = match_src.group(1) if match_src else ""
            elem_id = match_id.group(1) if match_id else "img1"
            html_elements.append(f'  <div><img id="{elem_id}" src="{src}" class="cp-img" alt="CodePi Image"></div>')

        elif line_str.startswith("create link"):
            match_text = re.search(r'create link "([^"]*)"', line_str)
            match_url = re.search(r'to "([^"]*)"', line_str)
            match_id = re.search(r'with name "([^"]*)"', line_str)
            text = match_text.group(1) if match_text else "Click Here"
            url = match_url.group(1) if match_url else "#"
            elem_id = match_id.group(1) if match_id else "link1"
            html_elements.append(f'  <div><a id="{elem_id}" href="{url}" class="cp-link" target="_blank">{text}</a></div>')

        elif line_str.startswith("make "):
            match_id = re.search(r'"([^"]*)"', line_str)
            if match_id:
                elem_id = match_id.group(1)
                selector = f"#{elem_id}"
                if selector not in css_rules:
                    css_rules[selector] = []
                
                # Support Background & Color Changes dynamically
                if " background " in line_str:
                    bg_color = line_str.split("background")[-1].strip()
                    css_rules[selector].append(f"background-color: {bg_color}")
                elif " color " in line_str:
                    color = line_str.split("color")[-1].strip()
                    css_rules[selector].append(f"color: {color}")

    # Advanced Styles for new elements
    if ".cp-card" not in css_rules:
        css_rules[".cp-card"] = ["background-color: #1e1e2e", "padding: 30px", "border-radius: 16px", "box-shadow: 0 10px 30px rgba(0,0,0,0.5)", "max-width: 400px", "margin: 20px auto", "text-align: center", "border: 1px solid #333"]
    if ".cp-btn" not in css_rules:
        css_rules[".cp-btn"] = ["padding: 12px 24px", "font-size: 16px", "border: none", "border-radius: 8px", "cursor: pointer", "font-weight: bold", "margin-top: 15px", "width: 100%"]
    if ".cp-img" not in css_rules:
        css_rules[".cp-img"] = ["width: 100%", "border-radius: 12px", "margin-bottom: 15px"]
    if ".cp-link" not in css_rules:
        css_rules[".cp-link"] = ["color: #00d2ff", "text-decoration: none", "font-weight: bold", "display: inline-block", "margin: 10px 0"]

    css_out = "<style>\n"
    for sel, rules in css_rules.items():
        css_out += f"{sel} {{\n  " + ";\n  ".join(rules) + ";\n}\n"
    css_out += "</style>"

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
    print(f"[SUCCESS] Compiled '{filename}' -> 'index.html'")
    return True

def start_server(port=8080):
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"\n[SERVE] CodePi Live Server running at: http://localhost:{port}")
        print("Press Ctrl+C to stop the server.\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[SERVE] Server stopped.")

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] in ["--help", "-h"]:
        print("Usage: ./codepi build <file.cp> | ./codepi serve <file.cp>")
    elif args[0] == "build":
        target = args[1] if len(args) > 1 else "app.cp"
        compile_cp(target)
    elif args[0] == "serve":
        target = args[1] if len(args) > 1 else "app.cp"
        if compile_cp(target):
            port = int(args[2]) if len(args) > 2 else 8080
            start_server(port)
    else:
        compile_cp(args[0])
