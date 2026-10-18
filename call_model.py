import os
from typing import cast

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionMessage,
    ChatCompletionMessageParam,
    ChatCompletionToolUnionParam,
)

from call_functions import avaialble_functions, call_function

_ = load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    raise RuntimeError("need api key")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


def call_model(
    messages: list[ChatCompletionMessageParam], verbose: bool = False
) -> tuple[ChatCompletionMessage, list[ChatCompletionMessageParam]]:
    response = client.chat.completions.create(
        model="openai/gpt-5.5",
        messages=messages,
        temperature=0,
        tools=cast(list[ChatCompletionToolUnionParam], avaialble_functions),
    )

    message = response.choices[0].message
    history_to_add: list[ChatCompletionMessageParam] = [
        cast(ChatCompletionMessageParam, message.to_dict())
    ]

    for tc in message.tool_calls or []:
        result_message = call_function(tc, verbose)
        if result_message.get("content") is None:
            raise ValueError("Error: tool result has no content")
        history_to_add.append(result_message)
        if verbose:
            print(f"-> {result_message['content']}")

    return message, history_to_add
