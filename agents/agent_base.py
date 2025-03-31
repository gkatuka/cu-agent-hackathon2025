import os
import openai
import sys
import json
import uuid
from pathlib import Path
from openai import AzureOpenAI
from abc import ABC, abstractmethod
from loguru import logger
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import find_dotenv, load_dotenv

#load environement variables
load_dotenv(find_dotenv())
logger.add("cu_ai_agent_system.log", level="INFO")

AZURE_AI_ENDPOINT = os.getenv("AZURE_AI_ENDPOINT")
AZURE_AI_API_VERSION = os.getenv("AZURE_AI_API_VERSION", "2024-12-01-preview")
AZURE_AI_API_VERSION = "2024-12-01-preview"
CREDENTIAL = DefaultAzureCredential()
TOKEN_PROVIDER = get_bearer_token_provider(CREDENTIAL, "https://cognitiveservices.azure.com/.default")

# Add the parent directory to the path to use shared modules
parent_dir = Path(Path.cwd()).parent
sys.path.append(str(parent_dir))
from python.content_understanding_client import AzureContentUnderstandingClient

class AgentBase(ABC):
    def __init__(self, name, max_retries=2, verbose=True):
        self.name = name
        self.max_retries = max_retries
        self.verbose = verbose

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

    def call_cu(self, analyzer_path, file_path):
        client = AzureContentUnderstandingClient(
            endpoint=AZURE_AI_ENDPOINT,
            api_version=AZURE_AI_API_VERSION,
            token_provider=TOKEN_PROVIDER
        )
        # Create analyzer
        analyzer_id = "cu-sample-" + str(uuid.uuid4())
        response = client.begin_create_analyzer(analyzer_id, analyzer_template_path=analyzer_path)
        result = client.poll_result(response)

        # Analyzer file
        logger.info(f"[{self.name}] Sending request to Content Understanding")
        response = client.begin_analyze(analyzer_id, file_location=file_path)
        result = client.poll_result(response)

        #save result to a file
        OUTPUT_FILEPATH = f'./data/outputs/{analyzer_id}'
        os.makedirs(os.path.dirname(OUTPUT_FILEPATH), exist_ok=True)
        with open (OUTPUT_FILEPATH, "w") as jf:
            json.dump(result, jf, indent=4)

        # print(json.dumps(result, indent=2))
        client.delete_analyzer(analyzer_id)
        return result
      
    def call_openai(self, messages, max_tokens,temperature=0.1):
        
    #     oai_client = AzureOpenAI(
    #     api_version="2024-12-01-preview",
    #     azure_endpoint="https://katukagloriarg8376509474.openai.azure.com/",
    #     azure_ad_token_provider=TOKEN_PROVIDER
    # )
        oai_client = AzureOpenAI(
        azure_endpoint=AZURE_AI_ENDPOINT,
        api_version=AZURE_AI_API_VERSION,
        azure_ad_token_provider=TOKEN_PROVIDER,
        )
        retries = 0
        
        while retries < self.max_retries:
            try: 
                if self.verbose:
                    logger.info(f"[{self.name}] Sending request to OpenAI") 
                    for msg in messages:
                        logger.debug(f"{msg['role']}: {msg['content']}")
                response = oai_client.chat.completions.create(
                    model = "gpt-4o",
                    messages = messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                reply = response.choices[0].message.content
                if self.verbose:
                    logger.info(f"[{self.name}] Recieved Response: {reply}")
                return reply
            except Exception as e:
                retries += 1
                logger.error(f"[{self.name}] Error during OpenAI call: {e}. Retry {retries}/{self.max_retries}")
        raise Exception(f"[{self.name}] Failed to get response from openAI after {self.max_retries}")

            