"""ai-excited-01 entry: copy the prepared image to the output directory.

The entry image (entry.jpg, shipped in this repo) is a whale-in-a-water-drop
sunset ocean scene. This program copies it byte-for-byte to the output
directory as entry.png, which is the artifact the competition judges.

Usage:
    python3 main.py

The output directory comes from the MAKEFUN_OUTPUT_DIR environment variable
(default /output when unset). The directory is created if needed.
"""

import hashlib
import os
import shutil
import sys

SOURCE_NAME = "entry.jpg"
OUTPUT_NAME = "entry.png"


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(output_dir, exist_ok=True)
    output = os.path.join(output_dir, OUTPUT_NAME)

    if not os.path.isfile(source):
        print(f"error: source image not found: {source}", file=sys.stderr)
        return 1

    shutil.copyfile(source, output)

    source_size = os.path.getsize(source)
    output_size = os.path.getsize(output)
    if source_size != output_size:
        print(f"error: size mismatch: source {source_size} bytes, "
              f"output {output_size} bytes", file=sys.stderr)
        return 1

    with open(source, "rb") as f:
        source_hash = hashlib.sha256(f.read()).hexdigest()
    with open(output, "rb") as f:
        output_hash = hashlib.sha256(f.read()).hexdigest()
    if source_hash != output_hash:
        print(f"error: output {output} does not match source {source}",
              file=sys.stderr)
        return 1

    print(f"wrote {output} ({os.path.getsize(output)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
