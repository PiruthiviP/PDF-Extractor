import fitz
import re
import requests

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


def write_to_google_sheets(chapter_titles, subchapter_titles, access_token, spreadsheet_id):
    # Prepare the data to write: Chapter in Column 1, Subchapter(s) in Column 2
    data_to_write = []

    # Loop through chapters and corresponding subchapters
    for chapter, subchapter in zip(chapter_titles, subchapter_titles):
        chapter_name = chapter[0]  # Extract chapter name (first item)
        subchapter_name = subchapter[0]  # Extract subchapter name (first item)
        # Add row with chapter and subchapter
        data_to_write.append([chapter_name, subchapter_name])

    # Construct the URL to interact with the Google Sheets API
    range_ = f'Sheet1!A1:B{len(data_to_write)}'  # Dynamically set the range based on the number of rows
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
    access_token = 'ya29.a0ARW5m7401rqN7_K5emUPMBb5FWzPJCWm0B-v6aVjEKJfpjvnA6RM84WTlV7w_8F7c1w5tu_Jt3nYLocc56YaMqwqZf3mCyauYFWiGWSQ6609ALnM7KC9LGT_jFCfYTBZh0qlLIO1yN10uwLUP5kqLkFnHc0iRtpDXEaRaEzBaCgYKAd8SARESFQHGX2Mi6GsBLjsgTv351HO15crrrg0175'  # Replace with your valid access token
    spreadsheet_id = '1Z1-Q7qciCu6mbkh9dma8aTC7956_psniytyN5chkUuc'  # Replace with your spreadsheet ID

    # Extract chapter and subchapter titles
    chapters, subchapters = find_chapter_and_subchapter_font_sizes(pdf_file_path, 
                                                                  min_chapter_font_size=18, max_chapter_font_size=36, 
                                                                  min_subchapter_font_size=12, max_subchapter_font_size=18)

    # Write extracted data to Google Sheets
    write_to_google_sheets(chapters, subchapters, access_token, spreadsheet_id)
