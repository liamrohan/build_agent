from functions.write_file import run_python_file


def test_run_python_file() -> None:
    cases: list[tuple[str, str, list[str] | None]] = [
        ("calculator", "main.py", None),
        ("calculator", "main.py", ["3 + 5"]),
        ("calculator", "tests.py", None),
        ("calculator", "../main.py", None),
        ("calculator", "nonexistent.py", None),
        ("calculator", "lorem.txt", None),
    ]
    for case in cases:
        working_dir, file_path, args = case
        r = run_python_file(working_dir, file_path, args)
        print(r)


test_run_python_file()
