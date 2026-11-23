"""Copy entry.png to the output directory.

Usage:
    python3 main.py

The source image is entry.png, located next to this file. The destination
directory comes from the MAKEFUN_OUTPUT_DIR environment variable and
defaults to /output when the variable is not set. The directory is
created if it does not exist yet. The copy is byte-for-byte identical.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(output_dir, exist_ok=True)

    destination = os.path.join(output_dir, "entry.png")
    shutil.copyfile(source, destination)
    return 0


if __name__ == "__main__":
    sys.exit(main())
