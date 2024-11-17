# Team eightA:  ESGjoy Website

## 🧑‍🎓Team Member(in alphabetic order)
Group A: Huang Shurui, Jiao Zijun, Liu Chengyan, Wan Xinyun

Group B: Jiang Xinfu, Shu Wenxuan, Sun Xinyi, Wang Hongsheng, Zou Yiyan

## 🌍Project Overview
  This project develops an innovative system to automate ESG information extraction from unstructured reports and analyze ESG performance in specific industries. Using large language models and a scoring framework, paired with detailed visualizations, the system streamlines data extraction, improves data quality, and delivers actionable insights for enhancing sustainability efforts.  

🎥 [Watch the Video Explanation](https://youtu.be/eJ5Dv__ui3Q)

  
## 💻Installation and Run

### Quick Access to the Cloud Deployment

No installation is required! You can directly access the system deployed on the cloud using the link below:  
🔗[Welcome to ESGjoy Website!](http://43.156.233.50:5001/)

<img width="800" alt="截屏2024-11-17 12 44 46" src="https://github.com/user-attachments/assets/0d9114b7-5f88-4734-98a6-8c0dcce7217c">

### Local Setup and Run

If you prefer running the project locally, follow these steps:

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

## 📊Features

The core features of this project include:

- **Automated ESG Data Extraction**: Extract key ESG-related information from unstructured files such as PDFs and text documents.
- **ESG Scoring System**: Provide comprehensive ESG scores covering three dimensions: Environment (E), Social (S), and Governance (G).
- **Dynamic Data Visualization Dashboard**: Display ESG performance through interactive charts and graphs.
- **User Authentication and Role Management**: Support user login/registration with role-based access for individuals, companies, and regulators.
- **Cloud-Based File Upload and Processing**: Enable secure file uploads and seamless data handling in the cloud environment.

## 🛠️GitHub Branch Structure

The repository is organized into multiple branches, each serving a specific purpose:

- **`main`**:  
  The primary branch containing runnable code and the stable version of the project. Use this branch to deploy the application.

- **`GroupA`**:  
  This branch includes all contributions and code developed by Team A, focusing on ESG  data extraction.

- **`GroupB`**:  
  This branch contains contributions and code developed by Team B, focusing on scoring system, visualization and system construction.

- **`data`**:  
  A dedicated branch for storing raw data, such as training reports, datasets, and related files used for machine learning or analysis. Note: This branch does not contain runnable code.


## 🤖Tech Stack

The technologies used in this project include:

- **Backend**: Flask, Dash
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MySQL
- **Machine Learning**: Python (pandas, numpy, scikit-learn, transformers etc.)
- **Cloud Platform**: Tencent Cloud



