import os
import json
import streamlit as st
# import pdfkit
import copy
# import markdown2
from io import BytesIO
from streamlit_chat import message
from pathlib import Path
from agents import AgentManager
from utils.logger import logger
from utils.formatters import format_schema2, markdown_to_pdf

st.set_page_config(
            page_title = "CU-powered AI Agent",
            layout="wide",
            page_icon="🤖",
        )

def main():
    custom_doc_markdown = None
    custom_analyzer_filepath = None

    with st.container():         
        st.title("CU-Powered Agentic System for EHR Document Creation")
        st.image("./images/cu-agent-flow.png",width= 1000)
        # st.markdown("""
        
        # In this multi-agent workflow, the user first uploads a PDF (containing EHR data) and an audio file. The system then performs the following steps:

        # 1. **Document Extraction**: Extracts structured content from the uploaded PDF using the CU Document Extraction Agent.
        # 2. **Schema Generation**: Generates a draft JSON schema based on the extracted content using the Schema Generation Agent.
        # 3. **Schema Editing**: Allows users to edit and refine the generated schema directly in the UI.
        # 4. **Speech Analytics**: Analyzes the uploaded audio file using the finalized schema to extract relevant information via the Speech Analytics Agent.
        # 5. **Document Creation**: Combines the analytics output and the finalized schema to produce a comprehensive EHR document using the Document Creation Agent.
        # 6. **Review and Export**: Enables users to review, edit, and export the final EHR document to PDF.

        # """)


    # Create three equally wide columns
    with st.container():  
        if "doc_markdown" not in st.session_state:
            st.session_state.doc_markdown = None
        if "custom_schema" not in st.session_state:
            st.session_state.custom_schema = None
        if "edit_mode" not in st.session_state:
            st.session_state.edit_mode = True
        if "updated_data" not in st.session_state:
            st.session_state.updated_data = None

        # We'll also store the final EHR doc markdown in session
        if "custom_doc_markdown" not in st.session_state:
            st.session_state.custom_doc_markdown = None
        col1, col2, col3 = st.columns([1, 2,2],  border=True, vertical_alignment="top")
        # --- Upload Sample EHR pdf file and audio file--- #
        save_folder = './input_data'
        os.mkdir(save_folder) if not os.path.exists(save_folder) else None
        pdf_filepath= None
        audio_filepath= None
        # Flags to track uploaded files
        pdf_uploaded = False
        audio_uploaded = False
        schema_created = False
    
        with col1:
            st.subheader("Upload Sample EHR pdf file")
            pdf_file = st.file_uploader("Choose a file to upload",type=["pdf"], accept_multiple_files=False)
            if pdf_file is not None:
                # st.write("filename:", pdf_file.name)
                pdf_filepath = Path(f"{save_folder}/{pdf_file.name}")
                with open(pdf_filepath , 'wb') as f: 
                    f.write(pdf_file.getbuffer())
                if pdf_filepath.exists():
                    st.success(f'File {pdf_file.name} is successfully uploaded!')
                    pdf_uploaded = True
            st.subheader("Upload audio file")
            audio_file = st.file_uploader("Choose a file to upload",  type=["wav", "mp3"], accept_multiple_files=False)
            if audio_file is not None:
                # st.write({"filename": audio_file.name, "filetype": audio_file.type, "filesize": audio_file.size})
                # st.write({"filename:" audio_file.name, "filetype": audio_file.type, "filesize": audio_file.size})
                audio_filepath = Path(f"{save_folder}/{audio_file.name}")
                with open(audio_filepath , 'wb') as f: 
                    f.write(audio_file.getbuffer())
                if audio_filepath.exists():
                    st.success(f'File {audio_file.name} is successfully uploaded!')
                    audio_uploaded = True

        # --- Start the AI Agent System --- #
        # if pdf_uploaded and audio_uploaded:
        with col2, st.container(height=1000):
                # if pdf_uploaded and audio_uploaded:
                # with st.container(): 
                if st.session_state.doc_markdown is None and pdf_uploaded and audio_uploaded: 
                    st.subheader("Auto-schema Generation from sample EHR pdf file")
                    st.badge("[CU_Agent for Document Extraction]", color="blue", icon="🌟")
                    st.write("This agent will extract the content from the uploaded sample EHR pdf file using CU.")
                    
                    with st.spinner("Starting CU Agent for document extraction..."):
                        docagent_manager = AgentManager()
                        docExtractionAgent = docagent_manager.get_agent("document_extraction")
                        doc_markdown = docExtractionAgent.execute(pdf_filepath)
                        st.session_state.doc_markdown = doc_markdown
                        st.success("Document Extraction Completed")
                    
                    st.badge("[LLM_Agent for Schema Generation]", color="green",icon="🌟")
                    st.write("This agent will use the extracted content from CU to automatic generate a schema in json format.")
                    with st.spinner("Starting Agent for Schema Generation..."):
                        schemaagent_manager = AgentManager(max_retries=2, verbose=True)
                        schemaGenerationAgent = schemaagent_manager.get_agent("schema_generator")
                        custom_schema = schemaGenerationAgent.execute(st.session_state.doc_markdown)
                        st.session_state.custom_schema = custom_schema
                        st.success("Schema Generation Completed")
            
                # field_count = len(fields)
                # --- Editing Schema --- #
                # with st.container(): 
                if st.session_state.custom_schema: 
                    pdf_uploaded = False
                    audio_uploaded = False
                    st.subheader("Edit Schema")
                    # json_str = str(st.session_state.custom_schema).strip().replace('\n', '').replace('    ', '')
                    # json_data = json.loads(json_str)

                    # fields = json_data.get("fields", {})
                    # field_count = len(fields)

                    # edit_mode: toggles whether we show the editable fields or not
                    # if "edit_mode" not in st.session_state:
                    #     st.session_state.edit_mode = True
                    # # updated_data: to store the final dictionary after user clicks "Save Changes"copy.deepcopy(json_data)
                    # if "updated_data" not in st.session_state:
                    #     st.session_state.updated_data = copy.deepcopy(json_data)


                    if st.session_state.updated_data is None:
                        # Convert custom_schema to string for parsing
                        json_str = str(st.session_state.custom_schema).strip().replace('\n', '').replace('    ', '')
                        json_data = json.loads(json_str)
                        st.session_state.updated_data = copy.deepcopy(json_data)

                    fields = st.session_state.updated_data.get("fields", {})
                    field_count = len(fields)

                    st.write(f"Number of fields: **{field_count}**")

                        # If we are in edit mode, display the text fields for editing
                    if st.session_state.edit_mode:
                        st.info("Edit the field names and descriptions below, then click 'Save Changes'.")

                        # Display editable inputs for each field
                        for field_name, field_details in fields.items():
                                st.subheader(f"Field: {field_name}")

                                # Text input for field name
                                st.text_input(
                                    label="Edit Field Name",
                                    value=field_name,
                                    key=f"{field_name}_field"
                                )

                                # Text area for description
                                st.text_area(
                                    label="Edit Description",
                                    value=field_details.get("description", ""),
                                    key=f"{field_name}_desc" ,
                                    height=80
                                )

                                # st.markdown("---")

                        # Save button
                        
                        if st.button("Save Changes"):
                            st.session_state.updated_data = build_updated_data(fields)
                            st.success("Edits saved! Below are your updated fields.")    
                            st.json(st.session_state.updated_data)
                            # st.session_state.edit_mode = False
                        else:
                            st.info("No edits have been made or saved yet.")

                        # Button to re-enable editing
                        if st.button("Edit Again"):
                                st.session_state.edit_mode = True
                        
                        if st.session_state.updated_data:
                        # else:
                            st.info("If you are satisfied with the schema, click 'Run' to generate CU results .")
                            # st.json(st.session_state.updated_data)
                            if st.button("Run"):
                                # Build an updated JSON-like structure
                                custom_schema = st.session_state.updated_data
                                custom_schema = json.dumps(custom_schema, indent=4)
                                print(custom_schema)
                                    # Switch edit mode off
                                # st.session_state.edit_mode = False
                                with st.spinner("preparing analyzer..."):
                                        generated_schema = format_schema2(custom_schema)#Todo: create a function to prepare analyzer
                                        # custom_analyzer = format_schema(generated_schema)
                                        custom_analyzer_filepath = "./templates/analyzer_templates/custom_analyzer.json"
                                        os.makedirs("./templates/analyzer_templates", exist_ok=True)
                                        with open(custom_analyzer_filepath, "w") as json_file:
                                            json.dump(generated_schema, json_file, indent=4)
                                        st.success("Analyzer prepared successfully!")
                                        # st.json(generated_schema)

        #     if st.session_state.updated_data:
    
                                with col3,st.container(height=1000):  
                                        st.subheader("Speech analytics and  EHR Document Creation")	
                                        st.badge("[CU_Agent for Speech Analytics]", color="blue", icon="🌟")
                                        st.write("This agent will analyze the content of the conversation and generate the results based on the fields from CU to automatic generate a schema in json format.")
                                        with st.spinner("Starting CU Agent for speech analytics..."):
                                            speechagent_manager = AgentManager()
                                            speechExtractionAgent = speechagent_manager.get_agent("speech_extraction")
                                            results = speechExtractionAgent.execute(custom_analyzer_filepath, audio_filepath)
                                            st.success("Feature Extraction Completed")
                                            st.json(results)
                                        st.badge("[LLM_Agent for Document Generation]", color="blue", icon="🌟")
                                        st.write("This agent will take the output from CU and a new EHR based on the provided conversation.")
                                        with st.spinner("Starting Document Creation..."):
                                            finaldocagent_manager = AgentManager(max_retries=2, verbose=True)
                                            finaldocagentAgent = finaldocagent_manager.get_agent("doc_creator")
                                            custom_doc_markdown = finaldocagentAgent.execute(results) 
                                            st.session_state.custom_doc_markdown = custom_doc_markdown
                                            st.markdown(custom_doc_markdown)
        with st.container():
                if "custom_doc_markdown" in st.session_state and st.session_state.custom_doc_markdown:  
                    # --- Edit document --- #
                    markdown_input = st.text_area("Edit the markdown content", value=st.session_state.custom_doc_markdown, height=500)
                    
                    if st.button("Save Document"): 
                        st.session_state.custom_doc_markdown = markdown_input
                        # Display the rendered Markdown
                        st.subheader("Preview")
                        st.markdown(markdown_input)  
                        # When the user clicks "Export to PDF", convert the HTML to PDF
                    if st.button("Export to PDF"):
                        output_folder = "./output_data"
                        os.mkdir(output_folder) if not os.path.exists(output_folder) else None
                        output_path = Path(f"{output_folder}/EHR_sample.pdf")
                        markdown_to_pdf(markdown_input, output_path)
                        st.success("Document Created and saved as PDF")
 
def build_updated_data(original_fields):
    """
    Build a new JSON structure from the user's edits in session state.
    We read the text inputs back from session state using known keys.
    """
    updated_data = {"fields": {}}
    for orig_name, field_details in original_fields.items():
        # The user-edited field name
        edited_name = st.session_state.get(f"{orig_name}_field", orig_name)
        # The user-edited description
        edited_description = st.session_state.get(
            f"{orig_name}_desc",
            field_details.get("description", "")
        )

        # Build the new structure
        updated_data["fields"][edited_name] = {
            "type": field_details.get("type", "string"),
            "method": field_details.get("method", "generate"),
            "description": edited_description
        }

        # If there's an enum, keep it in the updated data (only for demonstration)
        if "enum" in field_details:
            updated_data["fields"][edited_name]["enum"] = field_details["enum"]

    return updated_data

#     return updated_data
if __name__ == "__main__":
    main()