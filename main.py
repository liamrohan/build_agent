import argparse
import os
from collections.abc import Iterable
from typing import cast

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionToolUnionParam,
)

from call_functions import avaialble_functions, call_function
from prompts import system_prompt

_ = load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")


if not api_key:
    raise RuntimeError("need api key")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


def main():
    parser = argparse.ArgumentParser(description="chat")
    parser.add_argument("user_prompt", type=str, help="user prompt")
    parser.add_argument("--verbose", action="store_true", help="enable verbose")
    args = parser.parse_args()

    print("USER_PROMPT: ", args.user_prompt)
    print("SUSTEM_PROMPT: ", system_prompt)

    messages: Iterable[ChatCompletionMessageParam] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    response = client.chat.completions.create(
        model="openai/gpt-5.5",
        messages=messages,
        temperature=0,
        tools=cast(list[ChatCompletionToolUnionParam], avaialble_functions),
    )

    result = {}
    tool_calls = response.choices[0].message.tool_calls
    if tool_calls:
        for tc in tool_calls:
            print(tc)
            if tc != None:
                result = call_function(tc, True)
                print(result)
                if result["content"] == None or len(result["content"]) == 0:
                    raise Exception("Error: result is not as expected...")

    print(response.choices[0].message.content)

    if args.verbose:
        print(f"-> {result['content']}")
        # print(f"User prompt: {args.user_prompt}")
        # print(f"Prompt tokens: {response.usage.prompt_tokens}")
        # print(f"Response tokens: {response.usage.completion_tokens}")


if __name__ == "__main__":
    main()
