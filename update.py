import re
from pathlib import Path
from html import escape

def update_svg_ascii(svg_path, ascii_path):
    svg_content = Path(svg_path).read_text(encoding="utf-8")
    ascii_content = Path(ascii_path).read_text(encoding="utf-8")
    
    # Split ascii into lines
    ascii_lines = ascii_content.splitlines()
    
    # New Y coordinates for all lines in the file
    y_coords = []
    y = 52.0
    for i in range(len(ascii_lines)):
        y_coords.append(round(y, 2))
        y += 4.0
        
    # Generate tspan tags
    tspan_lines = []
    tspan_lines.append("") # Keep a blank line at the start if needed
    for i, line in enumerate(ascii_lines):
        y_val = y_coords[i]
        escaped_line = escape(line)
        tspan_lines.append(f'<tspan x="39" y="{y_val:.2f}" xml:space="preserve">{escaped_line}</tspan>')
    tspan_lines.append("") # Keep a blank line at the end
    
    new_tspan_block = "\n".join(tspan_lines)
    
    # Regex to find the <text x="30" y="0" class="ascii"> ... </text> block
    pattern = re.compile(
        r'(<text\s+x="30"\s+y="0"\s+class="ascii">).*?(</text>)',
        re.DOTALL
    )
    
    # Replace the block
    new_svg_content, count = pattern.subn(rf'\g<1>{new_tspan_block}\g<2>', svg_content)
    
    if count > 0:
        Path(svg_path).write_text(new_svg_content, encoding="utf-8")
        print(f"Successfully updated {svg_path} with {len(ascii_lines)} lines.")
    else:
        print(f"Error: Could not find the ASCII text block in {svg_path}.")

if __name__ == "__main__":
    ascii_file = "portrait.txt"
    update_svg_ascii("dark.svg", ascii_file)
    update_svg_ascii("light.svg", ascii_file)
