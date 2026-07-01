from __future__ import annotations

import argparse

import numpy as np

from vc_segcheck.pipeline import run_lcc_pipeline
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

    lcc = sub.add_parser("lcc", help="run Lamina-Continuity Check on lamina/confidence arrays")
    lcc.add_argument("--lamina-index", required=True, help="Path to 2D lamina index .npy")
    lcc.add_argument("--confidence", required=True, help="Path to 2D confidence .npy")
    lcc.add_argument("--out", required=True, help="Output directory")
    lcc.add_argument("--min-abs-delta-k", type=int, default=1)
    lcc.add_argument("--min-detection-confidence", type=float, default=0.0)
    lcc.add_argument("--min-gate-confidence", type=float, default=0.5)

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

    elif args.command == "lcc":
        lamina_index = np.load(args.lamina_index)
        confidence = np.load(args.confidence)

        summary = run_lcc_pipeline(
            lamina_index=lamina_index,
            confidence=confidence,
            out_dir=args.out,
            min_abs_delta_k=args.min_abs_delta_k,
            min_detection_confidence=args.min_detection_confidence,
            min_gate_confidence=args.min_gate_confidence,
            run_metadata={
                "entrypoint": "vc-segcheck lcc",
                "lamina_index": args.lamina_index,
                "confidence": args.confidence,
            },
        )

        print("OK vc-segcheck LCC pipeline complete")
        print(f"num_jump_edges={summary['counts']['num_jump_edges']}")
        print(f"num_accepted_edges={summary['counts']['num_accepted_edges']}")
        print(f"num_abstained_edges={summary['counts']['num_abstained_edges']}")
        print(f"num_regions={summary['counts']['num_regions']}")
        print(f"output={args.out}")


if __name__ == "__main__":
    main()
