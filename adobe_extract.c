#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
#include <jansson.h>

// Function to parse and print chapter names from JSON response
void parse_and_print_chapters(const char *json_response) {
    printf("im came here in the fun1");
    if (json_response == NULL) {
        fprintf(stderr, "No response from API\n");
        return;
    }

    json_error_t error;
    json_t *root = json_loads(json_response, 0, &error);
    if (!root) {
        fprintf(stderr, "Error parsing JSON: %s\n", error.text);
        return;
    }

    json_t *elements = json_object_get(root, "elements");
    if (!json_is_array(elements)) {
        fprintf(stderr, "Invalid JSON format: elements not found\n");
        json_decref(root);
        return;
    }

    size_t index;
    json_t *element;
    json_array_foreach(elements, index, element) {
        json_t *type = json_object_get(element, "type");
        if (json_is_string(type) && strcmp(json_string_value(type), "heading") == 0) {
            json_t *content = json_object_get(element, "content");
            if (json_is_array(content)) {
                json_t *text = json_array_get(content, 0);  // Get first content block
                if (json_is_string(text)) {
                    printf("Chapter: %s\n", json_string_value(text));
                }
            }
        }
    }

    json_decref(root);
}


// Function to upload the PDF and extract content using Adobe API
void extract_pdf(const char *access_token, const char *pdf_file_path) {
    printf("im came here in the fun2");
    if (!access_token) {
        fprintf(stderr, "Access token is NULL. Exiting.\n");
        return;
    }

    CURL *curl;
    CURLcode res;
    struct curl_slist *headers = NULL;
    const char *url = "https://pdf-services.adobe.io/v1/extract";

    curl = curl_easy_init();
    if (!curl) {
        fprintf(stderr, "CURL initialization failed.\n");
        return;
    }

    char auth_header[512];
    snprintf(auth_header, sizeof(auth_header), "Authorization: Bearer %s", access_token);
    headers = curl_slist_append(headers, auth_header);
    headers = curl_slist_append(headers, "Content-Type: multipart/form-data");
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

    curl_mime *mime;
    curl_mimepart *part;

    mime = curl_mime_init(curl);
    part = curl_mime_addpart(mime);
    curl_mime_name(part, "file");
    curl_mime_filedata(part, pdf_file_path);
    curl_easy_setopt(curl, CURLOPT_MIMEPOST, mime);

    char response[10240] = {0};  // Buffer for the response
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, response);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, (void *)strcat);

    res = curl_easy_perform(curl);
    if (res != CURLE_OK) {
        fprintf(stderr, "Request failed: %s\n", curl_easy_strerror(res));
    } else {
        // Parse and print chapter names
        parse_and_print_chapters(response);
    }

    curl_mime_free(mime);
    curl_easy_cleanup(curl);
}

// Function to get an access token from Adobe API
char* get_access_token(const char *client_id, const char *client_secret) {
    printf("im came here in the fun3");
    CURL *curl;
    CURLcode res;
    struct curl_slist *headers = NULL;
    char *token = NULL;
    
    const char* url = "https://ims-na1.adobelogin.com/ims/token/v2";
    
    char post_data[512];
    snprintf(post_data, sizeof(post_data), "grant_type=client_credentials&client_id=%s&client_secret=%s&scope=openid,creative_sdk", client_id, client_secret);

    curl = curl_easy_init();
    if (!curl) {
        fprintf(stderr, "CURL initialization failed.\n");
        return NULL;
    }

    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, post_data);

    headers = curl_slist_append(headers, "Content-Type: application/x-www-form-urlencoded");
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

    char response[2048] = {0};  // Buffer to store the response
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, response);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, (void *)strcat);

    res = curl_easy_perform(curl);
    if (res != CURLE_OK) {
        fprintf(stderr, "Request failed: %s\n", curl_easy_strerror(res));
        curl_easy_cleanup(curl);
        return NULL;
    }

    // Parse the response JSON to get the access token
    json_t *root;
    json_error_t error;
    root = json_loads(response, 0, &error);
    if (!root) {
        fprintf(stderr, "Error parsing JSON: %s\n", error.text);
        return NULL;
    }

    json_t *access_token = json_object_get(root, "access_token");
    if (!access_token) {
        fprintf(stderr, "Access token not found in the response\n");
        json_decref(root);
        return NULL;
    }

    token = strdup(json_string_value(access_token));
    json_decref(root);
    curl_easy_cleanup(curl);
    return token;
}

int main() {
    printf("im came here in the main fun");
    const char *client_id = "e46ae4a243604c2da00d4bb1ef369932";   // Replace with your Adobe API Client ID
    const char *client_secret = "p8e-FxXkRhLFKFF081tAsghxKanQ81vX4TO3";  // Replace with your Adobe API Client Secret
    const char *pdf_file = "file:///Users/piruthivi/pdf_pro/_OceanofPDF.com_An_Analysis_of_Albert_Banduras_Aggression_-_Jacqueline_Allan.pdf";

    // Get access token
    char *access_token = get_access_token(client_id, client_secret);
    if (!access_token) {
        fprintf(stderr, "Failed to get access token\n");
        return 1;
    }

    // Extract content from PDF
    extract_pdf(access_token, pdf_file);

    free(access_token);
    return 0;
}
