import fitz
import re

def extract_chapter_subchapter_content(filePath, min_chapter_font_size=18, max_chapter_font_size=36, min_subchapter_font_size=12, max_subchapter_font_size=18):
    pdf = fitz.open(filePath)
    chapter_titles = []  # List to store chapter titles within a certain font size range
    subchapter_titles = []  # List to store subchapter titles within a smaller font size range
    content_between_chapters = []  # List to store content between chapters and subchapters
    
    # Regex patterns to match chapter and subchapter titles
    chapter_pattern = r'^[A-Za-z0-9\s]+$'  # Catching general chapter-like patterns
    subchapter_pattern = r'^\d+\.'  # Match any number followed by a period at the start of the line
    
    # Extract the titles first
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
    
    # Now, extract content between chapters and subchapters
    chapter_index = 0
    subchapter_index = 0
    chapter_content = []  # To store content between a chapter and subchapter
    
    # Loop over pages to extract the content for each chapter and subchapter
    for page in pdf:
        dict = page.get_text("dict")
        blocks = dict["blocks"]
        
        for block in blocks:
            if "lines" in block.keys():
                spans = block['lines']
                
                for span in spans:
                    data = span['spans']
                    
                    for line in data:
                        text = line['text'].strip()
                        
                        # Check for chapter start
                        if chapter_index < len(chapter_titles) and chapter_titles[chapter_index][0] in text:
                            # If a chapter title is found, start capturing content
                            chapter_content.append(text)
                            chapter_index += 1
                            continue
                        
                        # Check for subchapter start
                        if subchapter_index < len(subchapter_titles) and subchapter_titles[subchapter_index][0] in text:
                            # If subchapter title is found, print the chapter and subchapter content
                            content_between_chapters.append({
                                "chapter": chapter_titles[chapter_index - 1][0],  # The last chapter found
                                "subchapter": subchapter_titles[subchapter_index][0],
                                "content": "\n".join(chapter_content)
                            })
                            # Reset for the next subchapter
                            chapter_content = [text]  # Start with the subchapter content
                            subchapter_index += 1
                            continue
                        
                        # If we are already capturing a chapter, just keep adding content
                        if chapter_index > 0:
                            chapter_content.append(text)
                    
                    # Once all subchapters for a chapter are found, break the loop
                    if subchapter_index >= len(subchapter_titles):
                        break
                if subchapter_index >= len(subchapter_titles):
                    break
            if subchapter_index >= len(subchapter_titles):
                break
    
    pdf.close()
    return content_between_chapters


# Main function to test
if __name__ == "__main__":
    pdf_file_path = "/Users/piruthivi/projects/PYPROJ/hello.pdf"
    
    # Extract content between chapters and subchapters
    content = extract_chapter_subchapter_content(pdf_file_path, 
                                                min_chapter_font_size=18, max_chapter_font_size=36, 
                                                min_subchapter_font_size=12, max_subchapter_font_size=18)
    
    # Print the content between chapters and subchapters
    for item in content:
        print(f"Chapter: {item['chapter']}")
        print(f"Subchapter: {item['subchapter']}")
        print(f"Content:\n{item['content']}")
        print("=" * 40)
