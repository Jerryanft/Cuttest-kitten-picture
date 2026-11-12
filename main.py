#!/usr/bin/env python3
"""Entry program for the make.fun "cutest picture" competition (cutest-picture-01).

The picture itself lives in ``entry.png`` right next to this file. All this
program does is deliver that picture to the grader: it copies the file,
byte for byte, into the output directory as ``entry.png``.

The output directory comes from the ``MAKEFUN_OUTPUT_DIR`` environment
variable when that is set (which is how local runs work); otherwise it
defaults to ``/output``, the location the grader provides in its container.

Only the Python standard library is used, and no network access is needed.
"""

import os
import shutil
from pathlib import Path


def main() -> None:
    # The source picture sits beside this script, wherever the repo was
    # checked out, so resolve it relative to this file rather than the
    # current working directory.
    source = Path(__file__).resolve().parent / "entry.png"

    # Pick the destination directory: the override from the environment if
    # present, falling back to the grader's default output location.
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

    # The grader hands us a writable output directory, but a local run may
    # point at one that does not exist yet, so create it just in case.
    output_dir.mkdir(parents=True, exist_ok=True)

    # Copy the picture unchanged — the judge should see exactly these bytes.
    shutil.copyfile(source, output_dir / "entry.png")


if __name__ == "__main__":
    main()
