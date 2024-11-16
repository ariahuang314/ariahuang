# ESGJOY
## Project Overview
  This project aims to develop an innovative system for automatically extracting ESG information from unstructured reports and conducting a comprehensive analysis of ESG performance in selected industries. By leveraging large language models and a scoring framework, combined with detailed front-end visualizations, the system not only simplifies the ESG data extraction process and enhances data quality but also provides valuable insights for companies to improve their sustainability efforts.
  
## Installation Guide

Follow the steps below to install and run the project:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/ariahuang314/groupproject.git
   ```
2. **Navigate to the project directory**:

   ```bash
   cd groupproject
   ```
## Repository Structure

### main

### config

### dash_app(1.0)

- Introduction: This project uses the Dash framework to build an interactive data visualization application. The app reads data from a local Excel file and dynamically updates visualizations based on user selection.

- Access the Application: After running the code cell that launches the Dash application, a local address (e.g., http://127.0.0.1:8050) will appear in the output. Click on this address or copy and paste it into the browser to access the app.

### dictionary

- Overview: The `dictionary` folder serves as a core resource hub for the script, containing classification rules and mappings between metrics and keywords.
- 
- Function: Facilitates metric categorization and keyword mapping, ensures data accuracy, and provides a foundation for downstream processes.-

### other

### output_metric

### pdf_processing

- Overview: This folder is a specialized modular toolkit designed for handling and managing PDF documents. It integrates functions for text extraction, cleaning, segmentation, and database interactions, providing technical support for efficient and systematic PDF processing.

- Function:
  - Text Processing and Extraction: Enables efficient extraction, cleaning and segmentation of PDF content.
  - File Management and Storage: Supports the uploading, storage, and organization of PDF files, generating corresponding text files for further use.
  - Database Interaction: Facilitates the storage of PDFs and their metadata in a structured database, ensuring reliable document management and retrieval.

### scr

- Overview: A comprehensive data processing and analysis module set, which is designed to extract, classify, and analyze Environmental, Social and Governance (ESG) metrics from documents. Codes in this folder integrate database management and scoring systems to enable the effective utilization of extracted data.

- Function:
  - ESG Data Extraction and Processing: Extracts the key ESG metrics from semi-structured text. Analyzes semantic and sentiment information using various models and generates both qualitative and quantitative data.
  - Data Integration and Analysis: Merges and processes qualitative and quantitative metrics and calculates semantic similarity. Also provides a basis for metric classification and analysis.
  - Scoring and Storage: Calculates ESG scores and ratings based on scoring rules, stores the results in a database and supports further data querying and industry benchmarking.

### static

### templates

- Overview: Mainly used to store HTML templates for the project. The templates inside define the structure and layout of the web pages, ensuring consistency in the user interface across the application.

- Function:
  - Interface Management: By separating HTML templates from application logic,  `templates` achieves a clear separation of concerns, making the project easier to maintain and update.
  - Unified Design: Provides a consistent layout and style for the project's user interface, enhancing the user experience.

## Notes
As a team, we have merged all the programs into the `main` branch to ensure all components function seamlessly as a whole. If you wish to explore the detailed processes of each sub-team, you can check the [`GroupA`](https://github.com/ariahuang314/groupproject/tree/GroupA_Data_Extraction) and [`GroupB`](https://github.com/ariahuang314/groupproject/tree/GroupB-ESG-estimate) branches.
