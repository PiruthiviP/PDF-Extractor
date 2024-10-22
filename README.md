# Universal-PDF-Extractor

# 📄 Universal PDF Extractor

**Universal PDF Extractor** is a powerful tool designed to seamlessly extract chapter names, subchapter names, and content from any PDF, and then upload the structured data into Google Sheets. 📊

The extracted data is organized with each **chapter** in the first column, each **subchapter** in the second column, and the corresponding **content** in the third column—providing clear and organized insights from your PDF documents.

---

## Table of Contents
1. [Features](#-features)
2. [Prerequisites](#-prerequisites)
3. [Installation](#-installation)
4. [Usage](#-usage)
5. [Compile and Run](#-compile-and-run)
6. [Example Output](#-example-output)
7. [Why Universal?](#-why-universal)

---
## 🚀 Features

- 📘 **Extracts Chapters, Subchapters, and Content** from PDFs effortlessly.
- 🌐 **Uploads extracted data directly to Google Sheets**.
- 📝 Supports a wide range of **PDF structures**.

---

## 🛠 Prerequisites

Before you can use **Universal PDF Extractor**, ensure you have the following installed:

- **Poppler**: A PDF rendering library used to extract text from PDF files.
- **libcurl**: A library for making HTTP requests to upload data to Google Sheets.
- **jansson**: A library used for JSON data manipulation.
- **Google API Access Token**: Required for connecting and uploading to Google Sheets.

---

## 🖥️ Installation

1. Install the required dependencies:

   ```bash
   brew install poppler
   brew install curl
   brew install jansson

  ## 📋 Usage
Update the following variables in the main C file:

- **pdf_path**: Path to the PDF file you wish to extract.
- **spreadsheet_id**: The ID of your Google Sheet where the data will be uploaded.
- **access_token**: Your Google API Access Token to authenticate the upload process.

## ⚙️ Compile and Run

- **Compile the program**:
  ```bash
  gcc -o pdf_extractor pdf_extractor.c `pkg-config --cflags --libs poppler-glib` -lcurl -ljansson

- **Run the tool**:
  ```bash
    ./pdf_extractor
-
  The extracted chapters, subchapters, and content will automatically be uploaded to the Google Sheet specified by the spreadsheet_id.

## 📊 Example Output
This is how the data will appear in the Google Sheet:

| **Chapter**   | **Subchapter**     | **Content**                  |
|---------------|--------------------|------------------------------|
| **Chapter 1** | **Subchapter 1.1** | Introductory Content         |
| **Chapter 1** | **Subchapter 1.2** | Detailed Content             |
| **Chapter 2** | **Subchapter 2.1** | Further Insights             |







 ##  🌍 Why Universal?
- **Versatility**: Works with a wide variety of PDF structures, making it suitable for different types of documents.
- **Efficiency**: Automatically extracts and uploads data, saving you time and effort.
- **User-Friendly**: Simple setup and usage, allowing users of all skill levels to benefit from the tool.


