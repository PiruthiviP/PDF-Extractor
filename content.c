#include <poppler/glib/poppler.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

// Function to check if a string is entirely uppercase
bool is_uppercase(const char *str) {
    while (*str) {
        if (!isupper(*str) && *str != ' ') // Ignore spaces
            return false;
        str++;
    }
    return true;
}

// Function to check if the string looks like a subchapter header (e.g., "1.1", "1.2")
bool is_subchapter(const char *line) {
    // Example: Start with a number followed by a period or a space
    if (isdigit(line[0]) && (line[1] == '.' || line[1] == ' ')) {
        return true;
    }
    
    // Check if the line is uppercase (e.g., a bold uppercase subchapter title)
    return is_uppercase(line);
}

// Function to extract content from the PDF
void extract_subchapter_content(PopplerDocument *document) {
    int num_pages = poppler_document_get_n_pages(document);
    bool capture = false;

    // Loop through each page
    for (int i = 0; i < num_pages; i++) {
        // Load the page
        PopplerPage *page = poppler_document_get_page(document, i);
        if (!page) {
            fprintf(stderr, "Error loading page %d\n", i);
            continue;
        }

        // Extract text from the page
        char *text = poppler_page_get_text(page);
        if (text) {
            // Split text into lines
            char *line = strtok(text, "\n");
            while (line != NULL) {
                // If the line looks like a subchapter header, print it as the start of a subchapter
                if (is_subchapter(line)) {
                    printf("\n%s\n", line);
                    capture = true;  // Start capturing content
                }

                // Print the content under the detected subchapter
                if (capture && !is_subchapter(line)) {
                    printf("%s\n", line);
                }

                line = strtok(NULL, "\n");
            }

            g_free(text); // Free the allocated text
        } else {
            printf("Failed to extract text from page %d\n", i + 1);
        }

        // Unref the page object
        g_object_unref(page);
    }
}

int main() {
    // Specify the correct PDF file path
    const char *pdf_file = "file:///Users/piruthivi/pdf_pro/_OceanofPDF.com_An_Analysis_of_Albert_Banduras_Aggression_-_Jacqueline_Allan.pdf";

    // Initialize GError
    GError *error = NULL;

    // Create a new Poppler document
    PopplerDocument *document = poppler_document_new_from_file(pdf_file, NULL, &error);
    if (!document) {
        fprintf(stderr, "Error opening PDF: %s\n", error->message);
        g_error_free(error);
        return 1;
    }

    // Extract content between detected subchapters
    extract_subchapter_content(document);

    // Unref the document object
    g_object_unref(document);

    return 0;
}
