#!/usr/bin/env python3
"""Entry program for the make.fun "cutest picture" competition (cutest-picture-01).

The picture itself lives in ``entry.png`` right next to this file. All this
program does is deliver that picture to the grader: it checks the file's
magic bytes really look like a PNG or a JPEG, then copies it, byte for byte,
into the output directory as ``entry.png``. The copy is atomic — it lands in
a temporary file in the output directory first and is renamed into place —
so the grader never sees a half-written picture.

The output directory comes from the ``MAKEFUN_OUTPUT_DIR`` environment
variable when that is set (which is how local runs work); otherwise it
defaults to ``/output``, the location the grader provides in its container.

Only the Python standard library is used, and no network access is needed.
"""

import os
import shutil
import sys
import tempfile
from pathlib import Path

# Magic numbers the gate's formats start with: the full 8-byte PNG
# signature, and the first three bytes of a JPEG (SOI plus a marker byte).
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"


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

    # Sanity-check the picture before copying it: the gate only accepts PNG
    # or JPEG, so fail loudly here rather than hand the grader a file it
    # would reject. Only the magic bytes are inspected, not the extension.
    with source.open("rb") as handle:
        header = handle.read(len(PNG_MAGIC))
    if not (header == PNG_MAGIC or header.startswith(JPEG_MAGIC)):
        sys.exit(
            f"error: {source} is not a PNG or JPEG image "
            f"(starts with {header!r}, not the PNG or JPEG magic bytes)"
        )

    # Copy the picture unchanged — the judge should see exactly these bytes —
    # but do it atomically: copy into a temporary file in the same directory
    # (so the rename stays on one filesystem), then rename it over the
    # destination in a single step.
    destination = output_dir / "entry.png"
    fd, temp_name = tempfile.mkstemp(dir=output_dir, prefix=".entry-", suffix=".tmp")
    os.close(fd)
    try:
        shutil.copyfile(source, temp_name)
        # mkstemp makes its file owner-only; match the source's permissions
        # so the renamed result is readable just like a plain copy would be.
        shutil.copymode(source, temp_name)
        os.replace(temp_name, destination)
    except BaseException:
        # Never leave the half-finished temporary file behind on failure.
        Path(temp_name).unlink(missing_ok=True)
        raise

    # One-line summary of what was delivered, for the run log.
    print(f"Copied {source} -> {destination} ({destination.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
