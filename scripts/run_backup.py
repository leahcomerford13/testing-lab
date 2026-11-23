"""Run a backup and report its progress and elapsed time."""

import argparse
import logging
from time import perf_counter

from backup import backup_files


def main():
    parser = argparse.ArgumentParser(description="Back up JSON configuration files")
    parser.add_argument("source", help="Folder containing the source files")
    parser.add_argument("destination", help="Folder for the backup files")
    args = parser.parse_args()

    # INFO reports routine progress; ERROR reports a problem.
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    start = perf_counter()  # Start the elapsed-time measurement.
    logging.info("Starting backup from %s", args.source)

    try:
        copied = backup_files(args.source, args.destination)
    except OSError as error:
        # A missing or inaccessible folder is an operational failure.
        logging.error("Backup failed after %.3f s: %s", perf_counter() - start, error)
        return 1  # Non-zero exit status signals failure.

    for path in copied:
        logging.info("Copied %s", path.name)
    logging.info("Backup completed in %.3f s; files copied: %d", perf_counter() - start, len(copied))
    return 0  # Exit status zero signals successful execution.


if __name__ == "__main__":
    raise SystemExit(main())
