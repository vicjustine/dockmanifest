"""Command line entry point for dockmanifest."""

import argparse
import csv
import sys

from .model import Manifest, Pallet


def load_pallets(path: str) -> list[Pallet]:
    """Read a staging CSV exported from the yard system."""
    pallets = []
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            pallets.append(
                Pallet(
                    pallet_id=row["pallet_id"],
                    destination=row["destination"],
                    weight_kg=float(row["weight_kg"]),
                    stackable=row["stackable"].strip().lower() == "true",
                )
            )
    return pallets


def build_manifest(trailer_id: str, axles: int, pallets: list[Pallet]) -> Manifest:
    manifest = Manifest(trailer_id=trailer_id, axles=axles)
    for pallet in pallets:
        manifest.add(pallet)
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="dockmanifest")
    parser.add_argument("csv_path", help="staging CSV from the yard system")
    parser.add_argument("--trailer", required=True)
    parser.add_argument("--axles", type=int, default=3, choices=[2, 3, 4])
    args = parser.parse_args(argv)

    manifest = build_manifest(args.trailer, args.axles, load_pallets(args.csv_path))

    print(f"Trailer {manifest.trailer_id} ({manifest.axles} axles)")
    print(f"  pallets      {len(manifest.pallets)}")
    print(f"  total weight {manifest.total_weight_kg():.1f} kg")
    print(f"  capacity     {manifest.capacity_kg()} kg")
    print(f"  stops        {', '.join(manifest.destinations())}")
    if manifest.is_overweight():
        print("  STATUS       OVERWEIGHT - do not dispatch")
        return 1
    print("  STATUS       within limits")
    return 0


if __name__ == "__main__":
    sys.exit(main())
