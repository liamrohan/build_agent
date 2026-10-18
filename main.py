import argparse
import time

from openai.types.chat import ChatCompletionMessageParam, ChatCompletionToolMessageParam

from call_model import call_model
from prompts import system_prompt


def main():
    parser = argparse.ArgumentParser(description="chat")
    parser.add_argument("user_prompt", type=str, help="user prompt")
    parser.add_argument("--verbose", action="store_true", help="enable verbose")
    args = parser.parse_args()

    messages: list[ChatCompletionMessageParam | ChatCompletionToolMessageParam] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(20):
        _, updated_messages = call_model(messages)
        messages.extend(updated_messages)
        print("sleeping for 4 seconds...")
        time.sleep(4)



if __name__ == "__main__":
    main()
