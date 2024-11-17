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
3. **Install the required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```
4. **OpenAI Keys**:

   Log in and obtain an OpenAI API key from [OpenAI API Keys](https://platform.openai.com/settings/organization/api-keys) when using the `llm_model.py` for metric extraction and standardization. [Click to get more specific instructions.](https://github.com/ariahuang314/groupproject/wiki/8-API-Keys)
   
## Repository Structure

### config

### dash_app

- Overview:

The objective of the dash app is to present data pertaining to a company's ___ESG___ performance. After uploading a company's ESG report through the front-end interface, the users will be presented with the company's ___ESG___ metrics, facilitating a comprehensive analysis of the company's sustainability performance.

- Function:

  - Real-time Data Visualization: Upon uploading a report, the application automatically presents the visualization charts.

  - Segmentation by ESG Metrics: The application supports segmentation of data across different ESG metrics, including environmental, social, and governance aspects, which allows users to gain detailed insights into the specific performance of each metric.

### dictionary

- Overview: The `dictionary` folder serves as a core resource hub for the script, containing classification rules and mappings between metrics and keywords.
- 
- Function: Facilitates metric categorization and keyword mapping, ensures data accuracy, and provides a foundation for downstream processes.-

### other

### output_metric

- Overview: Stores the results of data processing, focusing on organizing and preserving the analyzed and integrated metrics data. It's an output node in the data processing workflow, providing data for subsequent analysis and applications.

- Function:
  -Data Integration and Classification: Stores processed quantitative and qualitative metrics, categorizing them to lay the foundation for analysis and calculations.
  - Data Filtering and Optimization: Contains filtered and optimized metrics, ensuring relevance and reliability to support further analysis, modeling and standardization processes.


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

### main
- Overview: Responsible for managing the user interface, integrating data processing and coordinating backend logic. By combining multiple modules, it facilitates a complete workflow from data input to analytical output and provides users with an intuitive interaction experience.

- Function:
  - User Interaction and Routing Management: Offers functionalities such as multi-role login, data upload and result viewing. It also processes user requests through routing logic to ensure tailored services for different user types.  
  - Modular Function Invocation: Integrates various data processing modules, including PDF file processing, map visualization, model execution and data analysis.  
  - Data Management and Presentation: Enables data storage, querying, and updating through database integration. It presents analysis results and visualizations via frontend templates to support deeper insights and informed decision-making.
  - Security and Session Management: Implements session control for user authentication, information protection and role-based access management, ensuring system security and stability.

## Notes
As a team, we have merged all the programs into the `main` branch to ensure all components function seamlessly as a whole. If you wish to explore the detailed processes of each sub-team, you can check the [`GroupA`](https://github.com/ariahuang314/groupproject/tree/GroupA_Data_Extraction) and [`GroupB`](https://github.com/ariahuang314/groupproject/tree/GroupB-ESG-estimate) branches.
