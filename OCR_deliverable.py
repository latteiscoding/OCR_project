# Import necessary libraries
import pandas as pd
from google.cloud import vision
import sys
import pathlib
from pdf2image import convert_from_path
import io

#========================================
# Function to extract text within specified bounds from a document.
# Parameters:
# - document: The document object containing pages.
# - x1, y1: The top-left coordinates of the bounding box.
# - x2, y2: The bottom-right coordinates of the bounding box.
# Returns: Extracted text within the specified bounds as a single string.
def text_within(document, x1, y1, x2, y2): 
    text = ""
    # Iterate through pages in the document
    for page in document.pages:
        # Iterate through blocks in the page
        for block in page.blocks:
            # Iterate through paragraphs in the block
            for paragraph in block.paragraphs:
                # Iterate through words in the paragraph
                for word in paragraph.words:
                    # Iterate through symbols in the word
                    for symbol in word.symbols:
                        # Calculate min and max coordinates of the symbol
                        min_x = min(symbol.bounding_box.vertices[0].x, symbol.bounding_box.vertices[1].x, symbol.bounding_box.vertices[2].x, symbol.bounding_box.vertices[3].x)
                        max_x = max(symbol.bounding_box.vertices[0].x, symbol.bounding_box.vertices[1].x, symbol.bounding_box.vertices[2].x, symbol.bounding_box.vertices[3].x)
                        min_y = min(symbol.bounding_box.vertices[0].y, symbol.bounding_box.vertices[1].y, symbol.bounding_box.vertices[2].y, symbol.bounding_box.vertices[3].y)
                        max_y = max(symbol.bounding_box.vertices[0].y, symbol.bounding_box.vertices[1].y, symbol.bounding_box.vertices[2].y, symbol.bounding_box.vertices[3].y)
                        
                        # Check if symbol is within the specified bounds
                        if(min_x >= x1 and max_x <= x2 and min_y >= y1 and max_y <= y2):
                            text += symbol.text
                            # Handle space, tab, and newline characters based on detected_break type
                            if(symbol.property.detected_break.type in [1, 3]):
                                text += ' '
                            if(symbol.property.detected_break.type == 2):
                                text += '\t'
                            if(symbol.property.detected_break.type == 5):
                                text += '\n'
    return text

# Function to detect text in an image using Google Vision API.
# Parameters:
# - path: Path to the image file.
# Returns: The response from the text detection API call.
def detect_text(image_content):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)
    response = client.text_detection(image=image)

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    return response

# Function to convert PDF to text by first converting PDF pages to images
# and then using Google Vision API to detect text in those images.
# Parameters:
# - path: Path to the PDF file.
# Returns: A list of responses from the text detection API for each page.
def pdf_to_text(path):
    pdf_path = pathlib.Path(path)
    if not pdf_path.is_file():
        sys.exit("Invalid PDF path")
    
    # Convert PDF pages to images
    images = convert_from_path(str(pdf_path.resolve()), dpi=40)
    all_results = []
    for img in images:
        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # Extract text from the image bytes
        raw_response = detect_text(img_byte_arr)
        # Append the results for this page to all_results
        all_results.append(raw_response)
    return all_results

# Function to format detected text from all pages into a pandas DataFrame
# based on specified bounds for each column.
# Parameters:
# - all_results: List of responses from the text detection API.
# - bounds: List of bounding boxes for columns.
# Returns: A list of DataFrames, each representing formatted text for a page.
def page_format(all_results, bounds):
    dfs = []
    for result in all_results:
        texts = []
        max_row = 0
        for bound in bounds:
            # Extract and split text within bounds
            text = text_within(result.full_text_annotation, *bound)
            list_temp = text.split('\n')
            max_row = max(len(list_temp), max_row)
            texts.append(list_temp)
        # Ensure all columns have the same number of rows
        for text in texts:
            text.extend([''] * (max_row - len(text)))
        # Create and append a DataFrame for this page's results
        dfs.append(pd.DataFrame(texts).transpose())
    return dfs

# Main function to convert a PDF to an Excel file.
# Parameters:
# - path: Path to the PDF file.
# - bounds: Bounding boxes for columns to extract text.
# - out_path: Output path for the Excel file.
def pdf_to_xlsx(path, bounds, out_path):
    responses = pdf_to_text(path)
    dfs = page_format(responses, bounds)
    df_all = pd.concat(dfs)
    df_all.to_excel(out_path, index=False, header=False)

def main():
    # Sample usage: Convert a sample PDF to an Excel file
    print("Start converting...")
    bounds = [[0, 0, 1300/2, 10000], [1400/2, 0, 2000/2, 10000], [1880/2, 0, 9999, 10000]]
    input_path = "files/sample.pdf"
    output_path = "out/sample_out.xlsx"
    pdf_to_xlsx(input_path, bounds, output_path)
    print("Conversion done.")

if __name__ == "__main__":
    main()
