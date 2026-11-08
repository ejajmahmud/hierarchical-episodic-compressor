"""CLI for hierarchical-episodic-compressor."""
import sys
import argparse
from .compressor import HierarchicalEpisodicCompressor


def main():
    parser = argparse.ArgumentParser(description="Hierarchical Episodic Compressor CLI")
    parser.add_argument("--demo", action="store_true", help="Run episodic compression demonstration")
    args = parser.parse_args()

    if args.demo:
        comp = HierarchicalEpisodicCompressor(micro_chunk_size=3)
        for i in range(1, 10):
            comp.add_turn("user" if i % 2 == 1 else "assistant", f"Turn content {i}", action=f"tool_step_{i}" if i % 2 == 0 else None)
        ctx = comp.get_compressed_context()
        print(f"[+] Processed {ctx['total_raw_turns']} turns into hierarchical tiers:")
        print(f"    Macro Milestones: {ctx['macro_milestones']}")
        print(f"    Micro Summaries: {ctx['micro_summaries']}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
