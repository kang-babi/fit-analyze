from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from fit_exporter.analyzer import analyze_activity, analyze_activity_file
from fit_exporter.converter import parse_fit_file
from fit_exporter.reporter import format_analysis_text, write_report
from fit_exporter.validator import validate_activity_schema


def _write_output(data: Dict[str, Any], output_path: Path, pretty: bool) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as handle:
        if pretty:
            handle.write(json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8"))
        else:
            handle.write(json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _prompt_file_selection(input_dir: Path, extensions: list[str]) -> Path:
    input_dir.mkdir(parents=True, exist_ok=True)
    candidates = sorted(
        [path for path in input_dir.iterdir() if path.is_file() and path.suffix.lower() in extensions],
        key=lambda path: path.name.lower(),
    )
    if not candidates:
        raise SystemExit(
            f"No files found in {input_dir}. Add {', '.join(extensions)} files and rerun the command."
        )

    print(f"Select an input file from {input_dir}:")
    for index, candidate in enumerate(candidates, start=1):
        print(f"  {index}. {candidate.name}")

    while True:
        selection = input("Enter number: ").strip()
        if not selection.isdigit():
            print("Please enter a valid number.")
            continue
        selected_index = int(selection)
        if 1 <= selected_index <= len(candidates):
            return candidates[selected_index - 1]
        print(f"Please choose a number between 1 and {len(candidates)}.")


def _resolve_input_path(raw_input: str | None, default_dir: Path, extensions: list[str]) -> Path:
    if raw_input:
        candidate = Path(raw_input)
        if candidate.exists():
            return candidate
        candidate = default_dir / raw_input
        if candidate.exists():
            return candidate
        if candidate.suffix == "":
            for extension in extensions:
                candidate_with_ext = candidate.with_suffix(extension)
                if candidate_with_ext.exists():
                    return candidate_with_ext
        raise FileNotFoundError(f"Input file not found: {raw_input}")
    return _prompt_file_selection(default_dir, extensions)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Garmin FIT analysis application. Convert, analyze, and report on running activities."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    export_parser = subparsers.add_parser("export", help="Convert a Garmin FIT file to normalized JSON")
    export_parser.add_argument("input", nargs="?", help="Path to the .fit file")
    export_parser.add_argument(
        "-o",
        "--output",
        help="Output JSON file path",
        default=None,
    )
    export_parser.add_argument(
        "--pretty",
        action="store_true",
        help="Write human-readable JSON",
    )

    analyze_parser = subparsers.add_parser("analyze", help="Analyze a FIT or activity JSON file")
    analyze_parser.add_argument("input", nargs="?", help="Path to a .fit or .json activity file")
    analyze_parser.add_argument(
        "-o",
        "--output",
        help="Output analysis JSON file path",
        default=None,
    )
    analyze_parser.add_argument(
        "--report",
        nargs="?",
        const="",
        help="Also write a coaching report (optional path)",
        default=None,
    )
    analyze_parser.add_argument(
        "--pretty",
        action="store_true",
        help="Write human-readable analysis JSON",
    )

    report_parser = subparsers.add_parser("report", help="Generate a coaching report from activity or analysis JSON")
    report_parser.add_argument("input", nargs="?", help="Path to analysis JSON or normalized activity JSON")
    report_parser.add_argument(
        "-o",
        "--output",
        help="Output markdown report path",
        default=None,
    )

    return parser


def _maybe_load_activity(input_path: Path) -> Dict[str, Any]:
    if input_path.suffix.lower() == ".fit":
        return parse_fit_file(str(input_path))
    return _load_json(input_path)


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    command = args.command

    if command == "export":
        input_path = _resolve_input_path(args.input, Path("input"), [".fit"])
        output_path = Path(args.output) if args.output else Path("output") / input_path.stem / "activity.json"
        activity = parse_fit_file(str(input_path))
        _write_output(activity, output_path, bool(args.pretty))
        print(f"Exported activity JSON to {output_path}")
        return

    if command == "analyze":
        input_path = _resolve_input_path(args.input, Path("input"), [".fit", ".json"])
        output_path = Path(args.output) if args.output else Path("output") / input_path.stem / "analysis.json"
        activity = _maybe_load_activity(input_path)
        issues = validate_activity_schema(activity)
        if issues:
            print("Warning: activity JSON has validation issues:")
            for issue in issues:
                print(f"- {issue}")
        analysis = analyze_activity(activity)
        _write_output(analysis, output_path, bool(args.pretty))
        print(f"Wrote analysis JSON to {output_path}")
        if args.report is not None:
            report_output = Path(args.report) if args.report else Path("output") / input_path.stem / "report.md"
            report_text = format_analysis_text(analysis)
            write_report(report_text, report_output)
            print(f"Wrote coaching report to {report_output}")
        return

    if command == "report":
        input_path = _resolve_input_path(args.input, Path("input"), [".json"])
        output_path = Path(args.output) if args.output else Path("output") / input_path.stem / "report.md"
        if input_path.suffix.lower() == ".fit":
            raise ValueError("Report command accepts activity JSON or analysis JSON only.")
        content = _load_json(input_path)
        if content.get("recommendations") is not None:
            analysis = content
        else:
            analysis = analyze_activity(content)
        report_text = format_analysis_text(analysis)
        write_report(report_text, output_path)
        print(f"Wrote coaching report to {output_path}")
        return


if __name__ == "__main__":
    main()
