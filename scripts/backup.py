"""Copy JSON configuration files to a local backup directory."""

from pathlib import Path
from shutil import copy2


def backup_files(source_dir, destination_dir):
    """Copy direct-child .json files and return their destination paths."""
    source = Path(source_dir)
    destination = Path(destination_dir)

    # Reject a missing source before creating any output directories.
    if not source.is_dir():
        raise FileNotFoundError(f"Source directory not found: {source}")

    destination.mkdir(parents=True, exist_ok=True)
    copied = []

    # Look only at the files immediately inside the source directory.
    for path in sorted(source.iterdir()):
        # Do not copy notes, subdirectories or other file types.
        if path.is_file() and path.suffix == ".json":
            target = destination / path.name
            copy2(path, target)
            copied.append(target)

    # Report what was actually copied, not what we hoped to copy.
    return copied
