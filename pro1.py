import fitz
import re

def find_chapter_font_sizes(filePath, min_font_size=18, max_font_size=36):
    pdf = fitz.open(filePath)
    chapter_titles = []  # List to store chapter titles within a certain font size range
    
    # Regex pattern to match lines that are purely numbers (e.g., "8", "9", etc.)
    number_pattern = r'^\d+$'
    
    for page in pdf:
        dict = page.get_text("dict")
        blocks = dict["blocks"]
        
        for block in blocks:
            if "lines" in block.keys():
                spans = block['lines']
                
                for span in spans:
                    data = span['spans']
                    
                    for line in data:
                        font_size = line['size']
                        text = line['text'].strip()
                        
                        # Skip lines that are just numbers or unwanted prefixes
                        if re.match(number_pattern, text) or text.lower().startswith("text:"):
                            continue
                        
                        # Check if the font size is within the desired range for chapter names
                        if min_font_size <= font_size <= max_font_size:
                            chapter_titles.append((text, font_size))  # Store chapter title and font size
    
    pdf.close()
    return chapter_titles


# Main function to test
if __name__ == "__main__":
    pdf_file_path = "/Users/piruthivi/projects/PYPROJ/hello.pdf"
    
    # Define a range of font sizes for chapter titles
    chapters = find_chapter_font_sizes(pdf_file_path, min_font_size=18, max_font_size=36)
    
    # Print only the chapter titles without "Text:" or numbers
    for title, size in chapters:
        print(f"{title}")
