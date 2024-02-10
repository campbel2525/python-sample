from typing import List, TypedDict

import tiktoken
from langchain.schema import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from app.helpers import env_helpers, log_helpers
from app.enums.langchain_enums import LangchainRole
from config import langchain_config, settings

logger = log_helpers.setup_logger(__name__)


class MessagesType(TypedDict):
    role: str
    content: str


class LangchainSendChatService:
    def __init__(self, model_name: str, messages: List[MessagesType]):
        self.model_name = model_name
        self.messages = messages

        if self._check_model_name() is False:
            raise ValueError("model_name is invalid.")

    def _check_model_name(self) -> bool:
        if self.model_name not in langchain_config.USEABLE_MODEL_NAME:
            return False
        return True

    def send_message(
        self,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> str:
        langchain_messages = self._create_messages()
        if self._check_tokens(langchain_messages, max_tokens) is False:
            raise ValueError("model_name is invalid.")

        parameters = {
            "max_tokens": max_tokens,
            "model_name": self.model_name,
            "openai_api_key": settings.OPENAI_API_KEY,
            "temperature": temperature,
        }

        if env_helpers.is_local():
            logger.info(langchain_messages)
            print(langchain_messages)

        chat = ChatOpenAI(**parameters)
        result = chat.invoke(langchain_messages)
        return result.content

    def _check_tokens(
        self,
        langchain_messages: List[BaseMessage],
        max_tokens: int,
    ) -> bool:
        """
        token数のチェック
        """
        if len(langchain_messages) == 0:
            return False

        encode_name = langchain_config.ENCODE_NAME[self.model_name]

        tiktoken_enc = tiktoken.get_encoding(encode_name)

        total_tokens = 0
        for langchain_message in langchain_messages:
            tokens = tiktoken_enc.encode(langchain_message.content)
            total_tokens += len(tokens)

        return langchain_config.MAX_TOKEN[self.model_name] > (total_tokens + max_tokens)

    def _create_messages(self) -> List[BaseMessage]:
        langchain_messages: List[BaseMessage] = []
        for message in self.messages:
            if message["role"] == LangchainRole.AI.value:
                langchain_messages.append(AIMessage(content=message["content"]))
                continue

            if message["role"] == LangchainRole.HUMAN.value:
                langchain_messages.append(HumanMessage(content=message["content"]))
                continue

            if message["role"] == LangchainRole.SYSTEM.value:
                langchain_messages.append(SystemMessage(content=message["content"]))
                continue

        return langchain_messages
