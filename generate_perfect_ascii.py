import cv2
import numpy as np

def generate_perfect_ascii(image_path, output_path, width=90, height=53):
    # Read image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Error: Could not read image.")
        return False
        
    # Resize to target size (90 columns, 53 rows)
    img_resized = cv2.resize(img, (width, height), interpolation=cv2.INTER_LANCZOS4)
    
    # Apply CLAHE to enhance local contrast (brings out eyes, eyebrows, hair details)
    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
    img_equalized = clahe.apply(img_resized)
    
    # Custom character mapping to handle dark hair/shirt vs bright face vs black background
    ascii_lines = []
    for y in range(height):
        line = []
        for x in range(width):
            val = img_equalized[y, x]
            
            # Map values to characters to maximize detail contrast
            if val < 25:
                char = " "
            elif val < 45:
                char = "."
            elif val < 65:
                char = ":"
            elif val < 85:
                char = "-"
            elif val < 110:
                char = "="
            elif val < 135:
                char = "+"
            elif val < 165:
                char = "*"
            elif val < 195:
                char = "%"
            elif val < 225:
                char = "@"
            else:
                char = "#"
                
            line.append(char)
        ascii_lines.append("".join(line))
        
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(ascii_lines))
        
    print(f"Successfully generated perfect ASCII art and saved to {output_path}")
    return True

if __name__ == "__main__":
    img_path = "C:/Users/adity/.gemini/antigravity-ide/brain/f3d7af34-2f4b-4177-aaad-1ec42a3bc17a/media__1784256047852.jpg"
    generate_perfect_ascii(img_path, "portrait.txt")
