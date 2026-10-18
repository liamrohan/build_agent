import argparse

from openai.types.chat import ChatCompletionMessageParam

from call_model import call_model
from prompts import system_prompt


def main():
    parser = argparse.ArgumentParser(description="chat")
    parser.add_argument("user_prompt", type=str, help="user prompt")
    parser.add_argument("--verbose", action="store_true", help="enable verbose")
    args = parser.parse_args()

    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(20):
        message, updated_messages = call_model(messages, args.verbose)
        messages.extend(updated_messages)
        if not message.tool_calls:
            print("Final response:")
            print(message.content or "")
            return

    print("Error: agent reached the limit of 20 iterations without a final response.")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
