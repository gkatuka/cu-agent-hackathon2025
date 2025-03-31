from .agent_base import AgentBase
from loguru import logger

class CUDocAgent(AgentBase):
    def __init__(self, max_retries=2, verbose=True):
        super().__init__(name="CUDocAgent", max_retries=max_retries, verbose=verbose)

    def execute(self, doc_path):
        analyzer_path = r"C:\Users\katukagloria\source\ai_agent_cu\templates\analyzer_templates\content_document.json"
        doc_output = self.call_cu(analyzer_path=analyzer_path, file_path=doc_path)
        doc_content = doc_output['result']['contents'][0]['markdown']
        return doc_content
