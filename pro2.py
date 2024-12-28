import fitz
import re

def find_chapter_and_subchapter_font_sizes(filePath, min_chapter_font_size=18, max_chapter_font_size=36, min_subchapter_font_size=12, max_subchapter_font_size=18):
    pdf = fitz.open(filePath)
    chapter_titles = []  # List to store chapter titles within a certain font size range
    subchapter_titles = []  # List to store subchapter titles within a smaller font size range
    
    # Regex patterns to match chapter and subchapter titles
    chapter_pattern = r'^[A-Za-z0-9\s]+$'  # Catching general chapter-like patterns
    subchapter_pattern = r'^\d+\.'  # Match any number followed by a period at the start of the line
    
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
                        
                        # Skip lines that are just numbers or irrelevant text
                        if re.match(r'^\d+$', text):  # Skip pure numbers
                            continue
                        
                        # Check if the font size is within the desired range for chapter titles
                        if min_chapter_font_size <= font_size <= max_chapter_font_size:
                            if re.match(chapter_pattern, text):
                                chapter_titles.append((text, font_size))  # Store chapter title and font size
                        
                        # Check if the font size is within the desired range for subchapters
                        if min_subchapter_font_size <= font_size <= max_subchapter_font_size:
                            if re.match(subchapter_pattern, text):
                                subchapter_titles.append((text, font_size))  # Store subchapter title and font size
    
    pdf.close()
    return chapter_titles, subchapter_titles


# Main function to test
if __name__ == "__main__":
    pdf_file_path = "/Users/piruthivi/projects/PYPROJ/hello.pdf"
    
    # Define font size ranges for chapters and subchapters
    chapters, subchapters = find_chapter_and_subchapter_font_sizes(pdf_file_path, 
                                                                  min_chapter_font_size=18, max_chapter_font_size=36, 
                                                                  min_subchapter_font_size=12, max_subchapter_font_size=18)
    
    # Print chapter titles
    print("Chapter titles found within the specified font size range:")
    for title, size in chapters:
        print(f"Chapter: {title}")
    
    # Print subchapter titles
    print("\nSubchapter titles found within the specified font size range:")
    for title, size in subchapters:
        print(f"Subchapter: {title}")
