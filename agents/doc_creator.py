from .agent_base import AgentBase
from loguru import logger

class DocCreationAgent(AgentBase):
    def __init__(self, max_retries=2, verbose=True):
        super().__init__(name="DocGenerationAgent", max_retries=max_retries, verbose=verbose)

    def execute(self, speech_extracted_content):
        system_message = "Your are an AI Assistant that analyzes a JSON data and creates an EHR document based on the data."
        user_content =(
            """Organize related fields into sections based on their relevance to the document content.
            Format each section properly with a clear title and structured subsections if nededed.
            Convert lists into bullet points and tables into structured data. 
            Ensure all extracted fields retain their original information, without modification or omission.
            The goal is to create a structured document that is easy to read and understand.
            Return the output in a markdown format.
            """
            f"""user: \n
            {speech_extracted_content}
            output: \n
            """
        )
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_content}
        ]
        
        generated_schema = self.call_openai(messages, max_tokens= 1026)       
        return generated_schema