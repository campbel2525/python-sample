# from typing import List, Union

# import tiktoken
# from langchain.schema import AIMessage, HumanMessage, SystemMessage
# from langchain_openai import ChatOpenAI

# from config import openai_config, settings


# class Langchain:
#     def send_message(
#         self,
#         messages: list,
#         model_name: str,
#         temperature: float = 0.7,
#         max_tokens: int = 1000,
#     ) -> str:
#         if max_tokens not in openai_config.USEABLE_MODEL_NAME:
#             raise ValueError("max_tokens is invalid.")

#         langchain_messages = self._create_messages(messages)

#         if self._check_tokens(langchain_messages, model_name) is False:
#             return None

#         parameters = {
#             "max_tokens": max_tokens,
#             "model_name": model_name,
#             "openai_api_key": settings.OPENAI_API_KEY,
#             "temperature": temperature,
#         }

#         chat = ChatOpenAI(**parameters)
#         result = chat.invoke(langchain_messages)
#         return result.content

#     def _check_tokens(self, langchain_messages: list, model_name: str) -> bool:
#         """
#         token数のチェック
#         """
#         if len(langchain_messages) == 0:
#             return False

#         encode_name = openai_config.ENCODE_NAME[model_name]

#         tiktoken_enc = tiktoken.get_encoding(encode_name)

#         total_tokens = 0
#         for langchain_message in langchain_messages:
#             tokens = tiktoken_enc.encode(langchain_message.content)
#             total_tokens += len(tokens)

#         return openai_config.MAX_TOKEN[model_name] > total_tokens

#     def _create_messages(
#         self, messages: list
#     ) -> List[Union[AIMessage, HumanMessage, SystemMessage]]:
#         langchain_messages = []
#         for message in messages:
#             if message["role"] == "ai":
#                 langchain_messages.append(AIMessage(content=message["content"]))
#                 continue

#             if message["role"] == "human":
#                 langchain_messages.append(HumanMessage(content=message["content"]))
#                 continue

#             if message["role"] == "system":
#                 langchain_messages.append(SystemMessage(content=message["content"]))
#                 continue

#         return langchain_messages
