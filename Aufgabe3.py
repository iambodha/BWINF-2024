"""Task 3: choose route lengths with the 2024 endpoint-ranking heuristic."""
import argparse
from dataclasses import dataclass
from itertools import combinations
from math import comb
from input_data import read_text


@dataclass(frozen=True)
class RouteResult:
    routes: tuple[int, ...]
    covered: int
    total: int
    candidates: int
    available_candidates: int


def parse_input(text: str) -> list[tuple[int, int]]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        raise ValueError("Input is empty.")
    count = int(lines[0])
    if count < 1 or len(lines) != count + 1:
        raise ValueError("Expected a member count and one interval per member.")
    intervals = []
    for line in lines[1:]:
        start, end = map(int, line.split())
        if start < 0 or start > end:
            raise ValueError("Intervals must satisfy 0 <= minimum <= maximum.")
        intervals.append((start, end))
    return intervals


def choose_routes(intervals: list[tuple[int, int]], candidate_limit: int = 60) -> RouteResult:
    """Search up to three distinct endpoints; count each member once.

    A cap of 60 preserves the original heuristic; 0 searches every endpoint.
    Bit masks cache membership instead of rescanning every member per triple.
    """
    if not intervals or any(start < 0 or start > end for start, end in intervals):
        raise ValueError("Provide nonempty, ordered, nonnegative intervals.")
    if candidate_limit < 0:
        raise ValueError("Candidate limit must be nonnegative; use 0 for all endpoints.")
    endpoints = sorted({point for interval in intervals for point in interval})
    masks = {
        point: sum(1 << i for i, (start, end) in enumerate(intervals) if start <= point <= end)
        for point in endpoints
    }
    ranked = sorted(endpoints, key=lambda p: (masks[p].bit_count(), p), reverse=True)
    pool = ranked[:candidate_limit] if candidate_limit else ranked
    best_routes, best_count = (), -1
    for routes in combinations(pool, min(3, len(pool))):
        covered = 0
        for point in routes:
            covered |= masks[point]
        count = covered.bit_count()
        if count > best_count:
            best_routes, best_count = tuple(sorted(routes)), count
        if best_count == len(intervals):
            break
    return RouteResult(best_routes, best_count, len(intervals), len(pool), len(endpoints))


def plot_routes(intervals, result, output: str) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, max(3, min(10, len(intervals) * 0.3))))
    for i, (start, end) in enumerate(intervals, 1):
        ax.plot([start, end], [i, i], color="#64748b", linewidth=3)
        ax.scatter([start, end], [i, i], color="#64748b", s=16)
    for point in result.routes:
        ax.axvline(point, color="#0f766e", linestyle="--", label=f"Route {point}")
    ax.set(xlabel="Route length", ylabel="Member (input row)",
           title=f"Wandertag: {result.covered}/{result.total} members covered")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Input file path or explicit HTTP(S) URL")
    parser.add_argument("--candidate-limit", type=int, default=60,
                        help="Ranked endpoints to search (default: 60; 0: all, potentially slow)")
    parser.add_argument("--plot", metavar="FILE", help="Save a plot; requires matplotlib")
    args = parser.parse_args()
    try:
        intervals = parse_input(read_text(args.input))
        result = choose_routes(intervals, args.candidate_limit)
        exhaustive = result.candidates == result.available_candidates
        print(f"Search: {'all endpoints' if exhaustive else 'capped heuristic'} "
              f"({result.candidates}/{result.available_candidates} candidates; "
              f"up to {comb(result.candidates, min(3, result.candidates))} combinations)")
        print("Route lengths: " + ", ".join(map(str, result.routes)))
        print(f"Members covered: {result.covered}/{result.total}")
        for point in result.routes:
            members = [str(i) for i, (a, b) in enumerate(intervals, 1) if a <= point <= b]
            print(f"Route {point}: members {', '.join(members)}")
        print("Member IDs are 1-based input rows; each member is counted once.")
        if args.plot:
            plot_routes(intervals, result, args.plot)
            print(f"Plot saved to {args.plot}")
    except ImportError:
        parser.exit(2, "Error: plotting requires matplotlib; install requirements-plot.txt.\n")
    except (OSError, ValueError) as error:
        parser.exit(2, f"Error: {error}\n")


if __name__ == "__main__":
    main()
