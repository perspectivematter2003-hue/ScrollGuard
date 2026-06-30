from __future__ import annotations

import argparse

from vc_segcheck.sampler import run_cached_crop_profile_smoke


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="vc-segcheck",
        description="vc-segcheck Lamina-Continuity Check prototype",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    profile = sub.add_parser("profile", help="sample CT intensity profiles")
    profile.add_argument("--cached-crop", required=True, help="Path to local cached 2D .npy crop")
    profile.add_argument("--vertices", type=int, default=40)
    profile.add_argument("--axis", choices=["x", "y"], default="y")
    profile.add_argument("--half-width", type=int, default=15)
    profile.add_argument("--out", required=True)

    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.command == "profile":
        records = run_cached_crop_profile_smoke(
            cached_crop=args.cached_crop,
            vertices=args.vertices,
            out_dir=args.out,
            axis=args.axis,
            half_width=args.half_width,
        )
        print("OK vc-segcheck cached-crop profile smoke complete")
        print(f"profiles={len(records)}")
        print(f"output={args.out}")
        print("No Vesuvius server access used.")


if __name__ == "__main__":
    main()
