# **PDF EXTRACTOR**

## **Overview**
This script extracts content from a PDF file, identifies chapters and subchapters, and writes the extracted data to a Google Sheet. The data is structured as follows:
- **Column 1**: Chapter title
- **Column 2**: Subchapter title
- **Column 3**: Content between the chapter and subchapter

The content is split into smaller chunks (if necessary) to comply with Google Sheets' 50,000-character per cell limit.

---

## **Features**
- Extracts chapter and subchapter titles based on font size.
- Identifies content between chapters and subchapters.
- Splits long content into smaller chunks to prevent errors during insertion into Google Sheets.
- Writes the extracted data into a specified Google Sheet.

---

## **Requirements**
Before running the script, ensure you have the following dependencies installed:

1. **PyMuPDF**: Used for PDF extraction.
   - Install via pip: `pip install pymupdf`
   
2. **Requests**: Used to interact with the Google Sheets API.
   - Install via pip: `pip install requests`

3. **Google Sheets API**: You'll need access to the Google Sheets API with a valid OAuth 2.0 token.

---

## **Setup Guide**

### 1. **Install Dependencies**
Run the following commands to install the required libraries:

```bash  `pip install pymupdf requests`


### 2. **Get Google Sheets API Access**
To interact with Google Sheets using the API, you’ll need an OAuth 2.0 access token. Follow these steps:

1. Go to [Google Developers Console](https://console.developers.google.com/).
2. Create a new project.
3. Enable the **Google Sheets API** for your project.
4. Set up **OAuth 2.0 credentials** for a desktop application.
5. Download the credentials and use them to obtain an access token.

For token generation, you can use a service like `oauth2client` or authenticate through Google’s official libraries.

## 3. Update Script with Your Details

In the script, replace the following placeholders with your actual details:

- **`pdf_file_path`**: The path to the PDF file you want to process.
- **`access_token`**: Your valid OAuth 2.0 access token.
- **`spreadsheet_id`**: The ID of the Google Sheet where you want to insert the extracted data.

### Example:

```python
pdf_file_path = "/path/to/your/pdf/file.pdf"
access_token = "your_access_token"
spreadsheet_id = "your_google_sheet_id"
```


## 4. Run the Script

Once you've set up the details in the script, you can execute it to process the PDF and write the data to your Google Sheet.

### Command to Run:

```bash
python extract_to_sheets.py
```
## 5. Acknowledgements

This project uses the following tools and libraries:

- **PyMuPDF**: For PDF processing.
- **Google Sheets API**: For interacting with Google Sheets.

Let me know if further adjustments are needed!



