from app.enums import openai

# USEABLE_MODEL_NAME = [
#     "gpt-4-1106-preview",
#     "gpt-4",
#     "gpt-4-32k",
#     "gpt-3.5-turbo-1106",
# ]

MAX_TOKEN = {
    openai.UseableModelName.GPT4_1106_PREVIEW: 128000,
    openai.UseableModelName.GPT4: 8192,
    openai.UseableModelName.GPT4_32K: 32768,
    openai.UseableModelName.GPT35_TURBO_1106: 16385,
}

ENCODE_NAME = {
    openai.UseableModelName.GPT4_1106_PREVIEW: "cl100k_base",
    openai.UseableModelName.GPT4: "cl100k_base",
    openai.UseableModelName.GPT4_32K: "cl100k_base",
    openai.UseableModelName.GPT35_TURBO_1106: "cl100k_base",
}
