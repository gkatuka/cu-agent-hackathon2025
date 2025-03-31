from .agent_base import AgentBase
from loguru import logger

class CUSpeechAgent(AgentBase):
    def __init__(self, max_retries=2, verbose=True):
        super().__init__(name="CUSpeechAgent", max_retries=max_retries, verbose=verbose)

    def execute(self, analyzer_path, audio_path):
        doc_output = self.call_cu(analyzer_path=analyzer_path, file_path=audio_path)
        doc_content = doc_output['result']['contents'][0]['fields']
        return doc_content
