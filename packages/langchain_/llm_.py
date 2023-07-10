import os
from typing import Dict, List, Optional, Tuple, Union

import torch
from langchain.llms import OpenAI
from langchain.llms.base import LLM
from langchain.llms.utils import enforce_stop_tokens


class ChatLLM(LLM):
    max_token: int = 10000
    temperature: float = 0.1
    top_p = 0.9
    history = []
    tokenizer: object = None
    model: object = None

    def __init__(self):
        super().__init__()

    @property
    def _llm_type(self) -> str:
        return "ChatLLM"

    def _call(self,
              prompt: str,
              stop: Optional[List[str]] = None) -> str:
        
        response = '你好啊'
        self.history.append((prompt, response))

        return response