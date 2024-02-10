from app.enums.openai_enums import UseableOpenaiModel

USEABLE_MODEL_NAME = [
    UseableOpenaiModel.GPT_4_1106_PREVIEW.value,
    UseableOpenaiModel.GPT_4_TURBO_PREVIEW.value,
    # "gpt-4",
    # "gpt-4-32k",
    # "gpt-3.5-turbo-1106",
]

MAX_TOKEN = {
    UseableOpenaiModel.GPT_4_1106_PREVIEW.value: 128000,
    UseableOpenaiModel.GPT_4_TURBO_PREVIEW.value: 128000,
    # "gpt-4": 8192,
    # "gpt-4-32k": 32768,
    # "gpt-3.5-turbo-1106": 16385,
}

ENCODE_NAME = {
    UseableOpenaiModel.GPT_4_1106_PREVIEW.value: "cl100k_base",
    UseableOpenaiModel.GPT_4_TURBO_PREVIEW.value: "cl100k_base",
    # "gpt-4": "cl100k_base",
    # "gpt-4-32k": "cl100k_base",
    # "gpt-3.5-turbo-1106": "cl100k_base",
}
