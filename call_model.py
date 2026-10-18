import os
from typing import cast

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import (
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

def call_model(messages: list[ChatCompletionMessageParam], verbose: bool = False) -> tuple[ChatCompletionMessageParam, list[ChatCompletionMessageParam]]:
    print("MESSAGES_IN: \n", messages)
    history_to_add: list[ChatCompletionMessageParam] = []
    response = client.chat.completions.create(
        model="openai/gpt-5.5",
        messages=messages,
        temperature=0,
        tools=cast(list[ChatCompletionToolUnionParam], avaialble_functions),
    )

    tool_call_result = {}
    tool_calls = response.choices[0].message.tool_calls
    is_tool_calls = len(tool_calls) > 0 if tool_calls else False
    if is_tool_calls and tool_calls:
        for tc in tool_calls:
            if tc is not None:
                history_to_add.append({
                    "role": "assistant",
                    "content": f"I want to call {tc.function.name}..."
                })
                tool_call_result = call_function(tc, True)
                history_to_add.append(tool_call_result)
                content_val = tool_call_result.get("content")
                if content_val is None or content_val == "None":
                    raise Exception("Error: result is not as expected...")

                # return (tool_call_result, messages_copy)

    if verbose:
        print(f"-> {tool_call_result['content']}")

    return (history_to_add[-1], history_to_add)
