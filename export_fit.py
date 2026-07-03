from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from fit_exporter.converter import parse_fit_file


def _write_output(data: Dict[str, Any], output_path: Path, pretty: bool) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as handle:
        if pretty:
            handle.write(json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8"))
        else:
            handle.write(json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert Garmin FIT file to normalized JSON as defined by .skills/project.md"
    )
    parser.add_argument("input", help="Path to the .fit file")
    parser.add_argument(
        "-o",
        "--output",
        help="Output JSON file path",
        default="output/activity.json",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Write human-readable JSON",
    )
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    data = parse_fit_file(str(input_path))
    _write_output(data, output_path, bool(args.pretty))
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
