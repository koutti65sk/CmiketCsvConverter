from pathlib import Path


ROOT = Path(".")


IGNORE_DIRS = {
    ".venv",
    "__pycache__",
}

IGNORE_PREFIXES = (
    ".git",
)


def should_ignore(path):
    for part in path.parts:
        if part in IGNORE_DIRS:
            return True

        if part.startswith(IGNORE_PREFIXES):
            return True

    return False


def print_tree(path, prefix=""):
    items = sorted(
        [
            item
            for item in path.iterdir()
            if not should_ignore(item)
        ],
        key=lambda x: (x.is_file(), x.name.lower())
    )

    for index, item in enumerate(items):
        is_last = index == len(items) - 1

        connector = "└── " if is_last else "├── "
        print(prefix + connector + item.name)

        if item.is_dir():
            extension = "    " if is_last else "│   "
            print_tree(
                item,
                prefix + extension
            )


print(ROOT.resolve().name)
print_tree(ROOT)