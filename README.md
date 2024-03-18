# OCR_project

## Project Description
This Python application automates the extraction of text from scanned PDF files and organizes the extracted text into xls format. Leveraging the powerful OCR capabilities of **Google Cloud Vision API**, it provides an efficient solution for converting scanned documents into editable text, suitable for data analysis and archival purposes.

### Features
Converts scanned PDF files to Excel with accurate text recognition.
Supports specifying text extraction areas to organize text into columns.
Utilizes Google Cloud Vision API for high-accuracy OCR.
### Prerequisites
- Supported Python Versions: 3.8 to 3.12
- Google Cloud account with Vision API enabled
- Required Python packages: pandas, google-cloud-vision, pdf2image

## Environment Setup
1. Ensure Python of supported version is installed on your system.
2. Install the necessary Python libraries by running:
```
pip install pandas google-cloud-vision pdf2image
```
3. Install Poppler (required by pdf2image for PDF processing) for your operating system.

### Google Cloud Vision setup
For details, click [here](https://cloud.google.com/vision/docs/setup) for Complete document for Cloud Vision setup and cleanup.
1. Create a project in the Google Cloud Console -- [General guide to the console](https://support.google.com/cloud/answer/3465889?hl=en&ref_topic=3340599#zippy=%2Cget-started).
2. Enable the Vision API for your project -- [How to enable / disable an API](https://cloud.google.com/service-usage/docs/enable-disable)
3. Install and initialize the [Google Cloud CLI](https://cloud.google.com/sdk/gcloud)
   The following link provides instructions:

   [Install](https://cloud.google.com/sdk/docs/install) the Google Cloud CLI, then [initialize](https://cloud.google.com/sdk/docs/initializing) it by running the following command:
   
```
gcloud init
```
5. Set up authentication and access control
## Contact
For support or queries, contact zjg.elaine@gmail.com / bjwq2019@gmail.com
