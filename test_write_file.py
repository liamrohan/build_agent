from functions.write_file import write_file


def test_write_file() -> None:
    paths: list[tuple[str, str, str]] = [
        # ("calculator", "lorem_write.txt", "well hello there"),
        ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
        ("calculator", "pkg/morelorem.txt", "lorem ipsum dolar sit amet"),
        ("calculator", "/tmp/temp.txt", "this should not be allowed")
    ]

    for p in paths:
        working_dir, file_path, content = p
        r = write_file(working_dir, file_path, content)
        print(r)


test_write_file()

