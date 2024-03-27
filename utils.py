import os


def create_path_if_not_exists(path):
    """Create the directory and its parent directories if they don't exist."""
    try:
        os.makedirs(path)
        print(f"Created directory: {path}")
    except FileExistsError:
        print(f"Directory already exists: {path}")