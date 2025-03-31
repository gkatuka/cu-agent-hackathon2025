from .agent_base import AgentBase
from loguru import logger

class SchemaGenerationAgent(AgentBase):
    def __init__(self, max_retries=2, verbose=True):
        super().__init__(name="SchemaGenerationAgent", max_retries=max_retries, verbose=verbose)

    def execute(self, doc_extracted_content):
        system_message = "Your are an AI Assistant that generates a structured JSON schema from the extracted content of a document."
        user_content =(
            """Organize the extracted content of the document into sections to determine all the relevant fields and extract them as they appear in the document.
            There should be a maximum of 10 fields extracted from the document. Make sure to use only the values in the main categories to define the field schema.
            The 10 or less fields should be extracted based on the sections of the documents. Field names should be derived from the document's sections and labels ONLY.
            For each relevant field generate a one-sentence description for the field based on the content of that section. 
            For open-ended contents, assign a 'generate' method to the field. 
            For contents that require classification, assign a 'classify' method to the field and provide an enum list of possible values."
            All extracted data must be properly structured based on the document's content.
            The goal is to create a structure json that can be used to define a schema for the document.
            Each field will have only one method and description. 
            There can be no spaces of any kind in the field names.
            Here is an example of a schema in the expected JSON format:
            "fields": { 
                "fieldName1": {
                "type": "string",
                "method": "generate",
                "description": "<fieldDescription1>"
                },
                "<fieldName2>": {
                "type": "string",
                "method": "classify",
                "description": "<fieldDescription2>",
                "enum": [
                    "<enumValue1>",
                    "<enumValue2>", 
                    "<enumValue3>"
                ]
                }
            }
            Steps:\n
            1. Carefully examine the content and understand the structure, flow, and key points of the content.\n
            2. Identify 10 or less relevant categories that will be used to define a maximum of 10 fields of the schema. Use only the values in the main categories to define the field schema.\n
            3. Use all the reponses for each main category to create a comprehensive description relevant to the field.\n
            4. Carefully assign the method to each field based on the content and include enum for the classify method.\n
            5. Provide the output in JSON format with all the fields in the field dictionary only with no additional text or commentary.
             **Do not wrap the output in any code blocks such as ```json``` or ```markdown```.**\n
            
            Expected output: \n
            The field names are derived from the document's sections.
            The descriptions provide a good description of the fields.
            """
            f"""user: \n
            {doc_extracted_content}
            output: \n
            """
        )
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_content}
        ]
        
        generated_schema = self.call_openai(messages, max_tokens= 1026)       
        return generated_schema