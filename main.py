import os
import json
import argparse
from pathlib import Path
from agents import AgentManager
from utils.logger import logger
from utils.formatters import format_schema, markdown_to_pdf
from dotenv import load_dotenv
    


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="AutoCreate a Pdf document.")
    parser.add_argument(
        "--pdf", 
        type=str, 
        required=True, 
        default="./data/EHR_John_Smith.pdf",
        help="Path to the PDF file")
    
    parser.add_argument(
        "--audio", 
        type=str, 
        required=True, 
        default="./data/doctor_patient_extended_conversation.wav",
        help="Path to the audio file")
    
    parser.add_argument(
        "--output", 
        type=str, 
        default="./data/EHR_sample.pdf", 
        help="Path to save the pdf output")

    args = parser.parse_args()

    # check input files
    if not os.path.exists(args.audio):
        logger.error(f"Error: Audio file '{args.audio}' not found.")
        return
    if not os.path.exists(args.pdf):
        logger.error(f"Error: PDF file '{args.pdf}' not found.")
        return
    
    # input_doc = "./data/EHR_John_Smith.pdf"
    # input_audio = "./data/doctor_patient_extended_conversation.wav"
    input_doc = args.pdf
    input_audio = args.audio
    # load_dotenv()
    logger.info("Starting AI Agent System")
    logger.info("Starting Content Understanding for document extraction") 
    docagent_manager = AgentManager()
    docExtractionAgent = docagent_manager.get_agent("document_extraction")
    doc_markdown = docExtractionAgent.execute(input_doc)
    # print(doc_markdown)
    logger.info("Document Extraction Completed")

    logger.info("Starting Schema Generation")
    schemaagent_manager = AgentManager(max_retries=2, verbose=True)
    schemaGenerationAgent = schemaagent_manager.get_agent("schema_generator")
    custom_schema = schemaGenerationAgent.execute(doc_markdown)
    # print(custom_schema)
    logger.info("Schema Generation Completed")

    logger.info("Preparing Analyzer") #save analyzer to a tempfile
    generated_schema = format_schema(custom_schema)#Todo: create a function to prepare analyzer
    # custom_analyzer = format_schema(generated_schema)
    custom_analyzer_filepath = "./templates/analyzer_templates/custom_analyzer.json"
    with open(custom_analyzer_filepath, "w") as json_file:
        json.dump(generated_schema, json_file, indent=4)
    
    logger.info("Starting Content Understanding for speech analytics ")
    speechagent_manager = AgentManager()
    speechExtractionAgent = speechagent_manager.get_agent("speech_extraction")
    results = speechExtractionAgent.execute(custom_analyzer_filepath, input_audio)
    logger.info("Speech Extraction Completed")

    logger.info("Starting Document Creation")
    finaldocagent_manager = AgentManager(max_retries=2, verbose=True)
    finaldocagentAgent = finaldocagent_manager.get_agent("doc_creator")
    custom_doc_markdown = finaldocagentAgent.execute(results)
  
    markdown_to_pdf(custom_doc_markdown, args.output)
    # convert_to_pdf(custom_doc_markdown)
    logger.info("Document Created and saved as PDF")
    logger.info("CU AI Agent System Finished")


if __name__ == "__main__":
    main()