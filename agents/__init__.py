from .cuDocAgent import CUDocAgent
from .cuSpeechAgent import CUSpeechAgent
from .schemaGen import SchemaGenerationAgent
from .doc_creator import DocCreationAgent


class AgentManager:
    def __init__(self, max_retries=2, verbose=True):
        self.agents= {
            "document_extraction": CUDocAgent(max_retries=max_retries),
            "schema_generator": SchemaGenerationAgent(max_retries=max_retries, verbose=verbose),
            "speech_extraction": CUSpeechAgent(max_retries=max_retries),       
            "doc_creator": DocCreationAgent(max_retries=max_retries, verbose=verbose)
        }
    
    def get_agent(self, agent_name):
        agent= self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"Agent '{agent_name}' not found")
        return agent