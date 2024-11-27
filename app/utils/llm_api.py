from typing import List, Optional
from litellm import completion as _completion,embedding


def chat(messages: List, model: str = "gpt-4-0125-preview",
         stream: bool = False, tools: Optional[List] = None,
         max_tokens: Optional[int] = None):

    completion = _completion(model=model, messages=messages, tools=tools,
                             stream=stream, max_tokens=max_tokens)
    return completion


def generate(model: str, messages: list) -> str:
    response = chat(messages, model, stream=False)
    return response.choices[0].message.content


def generate_with_tools(model: str, messages: List, tools: List = None):
    response = chat(messages, model, tools=tools, stream=False)
    return response


def embeddings( input: list, model: str = "text-embedding-3-small"):
    response = embedding(model, input)
    return response


def format_message(text: str) -> List:
    messages = [{"content": text, "role": "user"}]
    return messages