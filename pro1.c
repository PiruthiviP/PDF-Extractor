#include <poppler/glib/poppler.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

// Function to check if a string is entirely uppercase
int is_uppercase(const char *str) {
    while (*str) {
        if (!isupper(*str) && *str != ' ') // Ignore spaces
            return 0;
        str++;
    }
    return 1;
}

// Function to check if a line could be a chapter title based on general heuristics
int is_possible_chapter_title(const char *line) {
    // List of common non-chapter titles to ignore
    const char *ignore_keywords[] = {
        "CONTENTS", "WAYS IN TO THE TEXT", "THE MACAT LIBRARY",
        "ABOUT THE AUTHOR", "KEY POINTS", "NOTES", NULL
    };

    // Check if the line is in the ignore list
    for (const char **keyword = ignore_keywords; *keyword != NULL; keyword++) {
        if (strcasecmp(line, *keyword) == 0) {
            return 0; // Ignore this line
        }
    }

    // Check if the line length is reasonable for a title
    if (strlen(line) < 3 || strlen(line) > 100) {
        return 0; // Skip lines that are too short or too long
    }

    // Check for common characteristics of titles
    if (is_uppercase(line) || 
        strstr(line, "Chapter") != NULL || 
        strstr(line, "CHAPTER") != NULL) {
        return 1; // Line has potential to be a title
    }

    return 0; // Not a title
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

    // Get the total number of pages
    int num_pages = poppler_document_get_n_pages(document);
    printf("Total pages: %d\n", num_pages);

    // Flag to determine if we are past the index page
    int past_index = 0;

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
       
        // Check if text extraction was successful
        if (text) {
            // Split text into lines (this is a heuristic approach)
            char *line = strtok(text, "\n");
            while (line != NULL) {
                // If we have found the index, start skipping lines
                if (past_index) {
                    // If we encounter a line that looks like a chapter title, print it
                    if (is_possible_chapter_title(line)) {
                        printf(" %s\n", line);  // Print only chapter names
                    }
                } else {
                    // Check if the line contains "Contents" or similar and set the flag
                    if (strstr(line, "CONTENTS") || strstr(line, "INDEX")) {
                        past_index = 1;  // Now we are past the index
                    }
                }

                line = strtok(NULL, "\n"); // Get the next line
            }

            g_free(text); // Free the allocated text
        } else {
            printf("Failed to extract text from page %d\n", i + 1);
        }

        // Unref the page object
        g_object_unref(page);
    }

    // Unref the document object
    g_object_unref(document);

    return 0;
}
