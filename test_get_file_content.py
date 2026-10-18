from functions.get_file_content import get_file_content

def test_get_file_content() -> None:
        file_paths: list[str] = ["lorem.txt", "main.py", "pkg/calculator.py", "/bin/cat", "pkg/does_not_exist.py"]
        for f in file_paths:
            result = get_file_content("calculator", f)
            print(f"{f} truncated: {'truncated' in result}")
            if f == "lorem.txt":
                continue
            print(result)


test_get_file_content()
        
