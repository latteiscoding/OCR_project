# OCR_project

## I. Project Description
This Python application automates the extraction of text from scanned PDF files and organizes the extracted text into xls format. Leveraging the powerful OCR capabilities of **Google Cloud Vision API**, it provides an efficient solution for converting scanned documents into editable text, suitable for data analysis and archival purposes.

### Features
Converts scanned PDF files to Excel with accurate text recognition.
Supports specifying text extraction areas to organize text into columns.
Utilizes Google Cloud Vision API for high-accuracy OCR.
### Prerequisites
- Supported Python Versions: 3.8 to 3.12
- Google Cloud account with Vision API enabled
- Required Python packages: pandas, google-cloud-vision, pdf2image

## II. Environment Setup
1. Ensure Python of supported version is installed on your system.
2. Install the necessary Python libraries if you do not have them by running:
```
pip install pandas pdf2image
```
3. Install Poppler (required by pdf2image for PDF processing) for your operating system
   ### For Windows
   Compared to downloading zip file and adding it to PATH, Anaconda is recommended to install Poppler.
   > Additional Notes: 1. Environment: It's a good practice to create a new conda environment for each project to manage dependencies more effectively. If you're working within a specific conda environment, make sure to activate it before installing Poppler with the command `conda activate your_environment_name`. 2. Updating Conda: It's also a good idea to ensure your conda installation is up to date before installing new packages. You can update conda by running `conda update -n base -c defaults conda`.
   #### Step 1: Open Anaconda Prompt
   Find the Anaconda Prompt from your Start menu and open it. It's recommended to run it as an administrator to avoid permission issues during the installation process.
   #### Step 2: Search for Poppler Package
   First, you might want to search for the available Poppler packages in the Anaconda repositories. You can do this by executing the following command:
   ```
   conda search poppler
   ```
   This command will list all the versions of Poppler available for installation via Anaconda.
   #### Step 3: Install Poppler
   Install Poppler by running the following command:
   ```
   conda install -c conda-forge poppler
   ```
   #### Step 4: Verify Installation
   After the installation completes, you can verify that Poppler has been installed correctly by checking its version. Type the following command in the Anaconda Prompt:
   ```
   poppler-utils --version
   ```

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
4. Set up authentication and access control
  If you plan to use the Vision API, you need to set up authentication. Any client application that uses the API must be authenticated and granted access to the requested resources. This section describes important authentication concepts and provides steps for setting it up. For more information, see the [Google Cloud authentication overview](https://cloud.google.com/docs/authentication).

   Generally there are 3 options for authentication: [Authentication with user accounts](https://cloud.google.com/vision/docs/setup#user), [Authentication with service accounts](https://cloud.google.com/vision/docs/setup#sa), [Access control with roles](https://cloud.google.com/vision/docs/setup#role).
   
   We recommend choosing **user accounts** for the authentication and the corresponding steps are as below. Feel free to go through the documents above if you prefer other authentications.
   #### Authentication with user accounts
   <u>We are going to choose client library user account authentication here</u>, if you prefer *REST command line user account authentication*, click [here](https://cloud.google.com/vision/docs/setup#rest-command-line-user-account-authentication).
   ##### Client library user account authentication
   To authenticate for client library calls, you use the gcloud CLI. The `gcloud auth application-default login` command logs you in to gcloud for application default credentials with your user account, which should be done before calling the API. The `gcloud auth application-default set-quota-project` command must be used to set your project for billing and quotas related to API calls. Normally, this is the same project used by your agent, and you supply the project ID for the project you created in steps above.

   The `GOOGLE_APPLICATION_CREDENTIALS` environment variable must **NOT** be set in order for your application default credentials to be used by client libraries.

   To create application default credentials for your local environment:
   ```
   gcloud auth application-default login
   gcloud auth application-default set-quota-project PROJECT_ID
   ```

5. Install the Vision API client library
   #### Install the client library
   >You might get error message if your pip is not up-to-date.
   Update pip using the following command:
   ```
   pip install --upgrade pip   
   ```
   Install the client library using the following command:
   ```
   pip install --upgrade google-cloud-vision
   ```
   #### Set up authentication
   For a local development environment, you can set up [ADC](https://cloud.google.com/docs/authentication/application-default-credentials) with the credentials that are associated with your Google Account:
   1. [Install and initialize the gcloud CLI](https://cloud.google.com/sdk/docs/install).

   When you initialize the gcloud CLI, be sure to specify a Google Cloud project in which you have permission to access the resources your application needs.

   2. Create your credential file:
   ```
   gcloud auth application-default login
   ```
   A sign-in screen appears. After you sign in, your credentials are stored in the [local credential file used by ADC](https://cloud.google.com/docs/authentication/application-default-credentials#personal).

## III. Usage
### Function Setup
- Change the `input_path` to the path of the pdf to be converted. Similiarly, Change `output_path` to the desired output file path.
- The function comes with a default scanning boundary. Feel free to tune `bounds` to fit your own needs.
### Run the function
After setting up everything above, we can now convert a scanned PDF to an Excel file by simply running the script with the following command:
```
python OCR_deliverable.py
```

## IV. Contact
For support or queries, contact zjg.elaine@gmail.com / bjwq2019@gmail.com
