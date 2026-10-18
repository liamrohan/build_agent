from functions.get_files_info import get_files_info

def test_get_files_info():
    paths: list[str] = [".", "pkg", "/bin", "../"]
    for p in paths:
        print(get_files_info("calculator", p))

test_get_files_info()
