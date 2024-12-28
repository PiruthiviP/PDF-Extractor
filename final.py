import fitz
import re
import requests

# Function to extract chapters and subchapters content
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
                            # If subchapter title is found, store the chapter and subchapter content
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


# Function to split content into smaller chunks for Google Sheets
def split_content(content, max_length=50000):
    # Split the content into chunks that are smaller than the maximum allowed length
    chunks = []
    while len(content) > max_length:
        # Find the last space within the max_length limit to split
        split_index = content.rfind(' ', 0, max_length)
        chunks.append(content[:split_index])
        content = content[split_index:].strip()
    chunks.append(content)  # Add the remaining content
    return chunks


# Function to write data to Google Sheets
def write_to_google_sheets(chapter_titles, subchapter_titles, content_between_chapters, access_token, spreadsheet_id):
    # Prepare the data to write: Chapter in Column 1, Subchapter(s) in Column 2, Content in Column 3
    data_to_write = []

    # Loop through chapters, subchapters, and corresponding content
    for content in content_between_chapters:
        chapter_name = content['chapter']  # Extract chapter name
        subchapter_name = content['subchapter']  # Extract subchapter name
        chapter_content = content['content']  # Extract chapter content
        
        # Split the content into smaller chunks if it's too large for a single cell
        content_chunks = split_content(chapter_content)
        
        # Add rows with chapter, subchapter, and content chunks
        for i, chunk in enumerate(content_chunks):
            row = [chapter_name, subchapter_name]
            row.append(chunk)  # Add the content chunk to the row
            data_to_write.append(row)

    # Construct the URL to interact with the Google Sheets API
    range_ = f'Sheet1!A1:C{len(data_to_write)}'  # Dynamically set the range based on the number of rows
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range_}?valueInputOption=RAW'

    # Prepare headers with authorization token
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Prepare the payload with the data to be written
    payload = {
        "range": range_,
        "majorDimension": "ROWS",
        "values": data_to_write
    }

    # Send the request to Google Sheets API
    response = requests.put(url, headers=headers, json=payload)

    # Check the response from the API
    if response.status_code == 200:
        print("Data successfully written to the Google Sheet!")
    else:
        print(f"Failed to write data: {response.content}")


# Main function to run the extraction and sheet update
if __name__ == "__main__":
    pdf_file_path = "/Users/piruthivi/projects/PYPROJ/hello.pdf"  # Update with your PDF path
    access_token = 'your token '  # Replace with your valid access token
    spreadsheet_id = 'your sheet id'  # Replace with your spreadsheet ID

    # Extract chapter and subchapter titles and their content
    content = extract_chapter_subchapter_content(pdf_file_path, 
                                                min_chapter_font_size=18, max_chapter_font_size=36, 
                                                min_subchapter_font_size=12, max_subchapter_font_size=18)
    
    # Write extracted data to Google Sheets
    write_to_google_sheets([], [], content, access_token, spreadsheet_id)
