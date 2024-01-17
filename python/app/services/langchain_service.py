from typing import List, Optional, Union

import tiktoken
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from config import settings


class Langchain:
    def send_message(
        self,
        messages: list,
        model_name: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> Optional[str]:
        langchain_messages = self._create_messages(messages)

        if self._check_tokens(langchain_messages, model_name) is False:
            return None

        parameters = {
            "max_tokens": max_tokens,
            "model_name": model_name,
            "openai_api_key": settings.OPENAI_API_KEY,
            "temperature": temperature,
        }

        chat = ChatOpenAI(**parameters)
        result = chat.invoke(langchain_messages)
        return result.content

    def _max_tokens_by_model_name(self, model_name: str) -> Optional[int]:
        if model_name == "gpt-4-1106-preview":
            return 128000

        if model_name == "gpt-4":
            return 8192

        if model_name == "gpt-4-32k":
            return 32768

        if model_name == "gpt-3.5-turbo-1106":
            return 16385

        return None

    def _encode_name_by_model_name(self, model_name: str) -> Optional[str]:
        if model_name == "gpt-4-1106-preview":
            return "cl100k_base"

        if model_name == "gpt-4":
            return "cl100k_base"

        if model_name == "gpt-4-32k":
            return "cl100k_base"

        if model_name == "gpt-3.5-turbo-1106":
            return "cl100k_base"

        return "cl100k_base"

    def _check_tokens(self, langchain_messages: list, model_name: str) -> bool:
        """
        token数のチェック
        """
        if len(langchain_messages) == 0:
            return False

        encode_name = self._encode_name_by_model_name(model_name)

        tiktoken_enc = tiktoken.get_encoding(encode_name)

        total_tokens = 0
        for langchain_message in langchain_messages:
            tokens = tiktoken_enc.encode(langchain_message.content)
            total_tokens += len(tokens)

        return self._max_tokens_by_model_name(model_name) > total_tokens

    def _create_messages(
        self, messages: list
    ) -> List[Union[AIMessage, HumanMessage, SystemMessage]]:
        langchain_messages = []
        for message in messages:
            if message["role"] == "ai":
                langchain_messages.append(AIMessage(content=message["content"]))
                continue

            if message["role"] == "human":
                langchain_messages.append(HumanMessage(content=message["content"]))
                continue

            if message["role"] == "system":
                langchain_messages.append(SystemMessage(content=message["content"]))
                continue

        return langchain_messages
