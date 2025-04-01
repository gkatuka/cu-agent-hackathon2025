# CU-powered Agentic System for patients records document creation
# MMI Hackathon 2025

 In this multi-agent workflow, the user first uploads a PDF (containing EHR data) and an audio file. The system then performs the following steps:

- **Document Extraction**: Extracts structured content from the uploaded PDF using the CU Document Extraction Agent.
- **Schema Generation**: Generates a draft JSON schema based on the extracted content using the Schema Generation Agent.
- **Schema Editing**: Allows users to edit and refine the generated schema directly in the UI.
- **Speech Analytics**: Analyzes the uploaded audio file using the finalized schema to extract relevant information via the Speech Analytics Agent.
- **Document Creation**: Combines the analytics output and the finalized schema to produce a comprehensive EHR document using the Document Creation Agent.
- **Review and Export**: Enables users to review, edit, and export the final EHR document to PDF.
  
## Getting started
1. **Navigate to Project Directory**:
   Change to the directory where your project files are located:
   ```
   cd "path to your project"
   ```
2. **Set Enviromental Variables**
    Create .env fill and add your AZURE_AI_ENDPOINT from your Azure portal Azure AI Services instance. see `env.txt` 

3. **Create a Virtual Environment**:
   Run the following command to create a virtual environment (Please use python 3.10):
   ```
   python -m venv venv
   ```
   This will create a folder named `venv` in your project directory.

4. **Activate the Virtual Environment**:
   Use the following command to activate the virtual environment:
   ```
   venv\Scripts\activate
   ```
   After activation, your command prompt will show `(venv)` at the beginning of the line.

5. **Install Required Packages**:
   Use `pip` to install the dependencies listed in `requirements.txt`:
   ```
   pip install -r requirements.txt
   ```
6. **Run the following command**:
   ```
   python main.py --pdf  input_data/EHR_John_Smith.pdf --audio input_data/doctor_patient_extended_conversation.wav
   ```
   **OR**
   
8. **Run the streamlit Application**:
   Start your Streamlit app by running:
   ```
   streamlit run app.py
   ```
  **OR
8. **Deactivate the Virtual Environment**:
   When done, deactivate the virtual environment using:
   ```
   deactivate
