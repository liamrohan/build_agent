import copy
import io
import os
import unittest
from contextlib import redirect_stdout
from types import SimpleNamespace
from unittest.mock import patch

from openai.types.chat import ChatCompletionMessage

with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}):
    import call_model
    import main


def tool_message() -> ChatCompletionMessage:
    return ChatCompletionMessage(
        role="assistant",
        content=None,
        tool_calls=[
            {
                "id": call_id,
                "type": "function",
                "function": {
                    "name": "get_files_info",
                    "arguments": '{"directory": "."}',
                },
            }
            for call_id in ("call_first", "call_second")
        ],
    )


class AgentLoopTests(unittest.TestCase):
    def test_tool_requests_precede_all_matching_results_in_next_request(self):
        requested = tool_message()
        final = ChatCompletionMessage(role="assistant", content="The result is printed.")
        responses = [requested, final]
        requests = []

        def create(**kwargs):
            requests.append(copy.deepcopy(kwargs["messages"]))
            return SimpleNamespace(
                choices=[SimpleNamespace(message=responses.pop(0))]
            )

        def execute(tc, verbose):
            return {"role": "tool", "tool_call_id": tc.id, "content": "file listing"}

        messages = [{"role": "user", "content": "Explain the calculator."}]
        with (
            patch.object(call_model.client.chat.completions, "create", side_effect=create),
            patch.object(call_model, "call_function", side_effect=execute),
        ):
            _, history = call_model.call_model(messages)
            messages.extend(history)
            message, final_history = call_model.call_model(messages, verbose=True)

        self.assertEqual([m["role"] for m in requests[1]], ["user", "assistant", "tool", "tool"])
        self.assertEqual(requests[1][1], requested.to_dict())
        self.assertEqual(
            [m["tool_call_id"] for m in requests[1][2:]],
            [tc.id for tc in requested.tool_calls],
        )
        self.assertEqual(message.content, final.content)
        self.assertEqual(final_history, [final.to_dict()])

    def test_main_stops_after_final_response_and_passes_history(self):
        requested = tool_message()
        final = ChatCompletionMessage(role="assistant", content="The result is printed.")
        history = [requested.to_dict()]
        calls = []

        def model(messages, verbose):
            calls.append(copy.deepcopy(messages))
            if len(calls) == 1:
                return requested, history
            return final, [final.to_dict()]

        output = io.StringIO()
        with (
            patch("sys.argv", ["main.py", "Explain the calculator.", "--verbose"]),
            patch.object(main, "call_model", side_effect=model) as mocked,
            redirect_stdout(output),
        ):
            main.main()

        self.assertEqual(mocked.call_count, 2)
        self.assertEqual(calls[1], calls[0] + history)
        self.assertTrue(mocked.call_args.args[1])
        self.assertIn("Final response:\nThe result is printed.", output.getvalue())

    def test_main_exits_with_failure_after_twenty_iterations(self):
        requested = tool_message()
        output = io.StringIO()
        with (
            patch("sys.argv", ["main.py", "Keep working"]),
            patch.object(main, "call_model", return_value=(requested, [])) as mocked,
            redirect_stdout(output),
            self.assertRaises(SystemExit) as error,
        ):
            main.main()

        self.assertEqual(mocked.call_count, 20)
        self.assertEqual(error.exception.code, 1)
        self.assertIn("20 iterations without a final response", output.getvalue())


if __name__ == "__main__":
    unittest.main()
