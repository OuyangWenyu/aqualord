import argparse
import json
import sys

from .opportunities import build_empty_result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aqualord")
    subparsers = parser.add_subparsers(dest="command", required=True)

    opportunities = subparsers.add_parser(
        "opportunities",
        help="Estimate near-term observation opportunities for Query GeoJSON.",
    )
    opportunities.add_argument("--geo", required=True, help="Path to Query GeoJSON.")
    opportunities.add_argument("--hours", type=int, default=48, help="Future query window in hours.")
    opportunities.add_argument(
        "--start",
        help="UTC ISO-8601 start time for deterministic opportunity windows.",
    )
    opportunities.add_argument("--format", choices=["json"], default="json")
    opportunities.add_argument(
        "--orbit-provider",
        choices=["none", "fixture", "celestrak"],
        default="none",
        help="Orbit provider to use for opportunity detection.",
    )
    opportunities.add_argument(
        "--cache-dir",
        default=".aqualord-cache",
        help="Cache directory for live orbit providers.",
    )

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "opportunities":
        result = build_empty_result(
            args.geo,
            args.hours,
            orbit_provider=args.orbit_provider,
            start=args.start,
            cache_dir=args.cache_dir,
        )
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0

    parser.error(f"Unsupported command: {args.command}")
    return 2
