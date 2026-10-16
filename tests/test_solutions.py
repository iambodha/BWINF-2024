"""Offline regression tests and small independent reference searches."""

import importlib
from itertools import combinations, product
from math import lcm
from pathlib import Path
import random
import subprocess
import sys
import unittest
from unittest.mock import patch

import Aufgabe2 as ranking
import Aufgabe3 as hiking
import Aufgabe5 as tomb

ROOT = Path(__file__).resolve().parents[1]


def earliest_arrival(periods):
    """Discrete-time reachability oracle, independent of the backtracking code."""
    states = {0}  # Outside the corridor.
    for time in range(2 * lcm(*periods) * (len(periods) + 1) + 1):
        states = {i for i in states if i == 0 or (time // periods[i - 1]) % 2 == 1}
        reachable = set(states)
        frontier = list(states)
        while frontier:
            section = frontier.pop()
            if section == len(periods):
                return time
            for neighbour in (section - 1, section + 1):
                if 0 <= neighbour <= len(periods) and neighbour not in reachable:
                    if neighbour == 0 or (time // periods[neighbour - 1]) % 2 == 1:
                        reachable.add(neighbour)
                        frontier.append(neighbour)
        states = reachable
    return None


class RankingTests(unittest.TestCase):
    def test_statement_example_ignores_unselected_conflict(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as directory:
            source = Path(directory) / "ranking.txt"
            source.write_text("4 7 5\nB < A < D < F\nD < F < G\nA < E < D < C\nG < F < C\nB C D E F\n")
            self.assertEqual(ranking.find_good_ordering(str(source)), "B E D F C")

    def test_bad_header_and_selection(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as directory:
            source = Path(directory) / "ranking.txt"
            for text in ("", "0 2 1\nA", "1 2 2\nA < B\nA A", "1 2 2\nA B\nA B"):
                source.write_text(text)
                with self.subTest(text=text), self.assertRaises(ValueError):
                    ranking.read_input(str(source))

    def test_offline_example(self):
        self.assertEqual(ranking.find_good_ordering(str(ROOT / "examples/schwierigkeiten.txt")), "A C D E")

    def test_cycle(self):
        self.assertEqual(ranking.find_good_ordering(str(ROOT / "examples/schwierigkeiten-cycle.txt")),
                         "NO GOOD ORDERING POSSIBLE")

    def test_omitted_middle_task_does_not_erase_order(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as directory:
            source = Path(directory) / "ranking.txt"
            source.write_text("1 3 2\nZ < X < A\nA Z\n")
            self.assertEqual(ranking.find_good_ordering(str(source)), "Z A")

    def test_sort_does_not_consume_graph(self):
        graph, degrees = ranking.build_graph([("A", "B"), ("A", "B")], {"A", "B", "C"})
        self.assertEqual(ranking.topological_sort(graph, degrees, degrees), ["A", "B", "C"])
        self.assertEqual(ranking.topological_sort(graph, degrees, degrees), ["A", "B", "C"])


class HikingTests(unittest.TestCase):
    def test_example(self):
        data = hiking.parse_input((ROOT / "examples/wandern.txt").read_text())
        result = hiking.choose_routes(data)
        self.assertEqual((result.routes, result.covered), ((3, 7, 11), 6))

    def test_count_overlapping_members_once(self):
        self.assertEqual(hiking.choose_routes([(1, 10), (2, 9), (3, 8)]).covered, 3)

    def test_single_endpoint(self):
        result = hiking.choose_routes([(4, 4), (4, 4)])
        self.assertEqual((result.routes, result.covered), ((4,), 2))

    def test_exact_mode_against_integer_brute_force(self):
        rng = random.Random(43)
        for _ in range(50):
            intervals = [tuple(sorted((rng.randrange(6), rng.randrange(6)))) for _ in range(8)]
            expected = max(sum(any(a <= point <= b for point in routes) for a, b in intervals)
                           for routes in combinations(range(6), 3))
            self.assertEqual(hiking.choose_routes(intervals, 0).covered, expected)

    def test_candidate_cap_can_lose_coverage(self):
        intervals = [(0, 0)] * 4 + [(10, 10)] * 3 + [(20, 20)] * 2
        self.assertEqual(hiking.choose_routes(intervals, 2).covered, 7)
        self.assertEqual(hiking.choose_routes(intervals, 0).covered, 9)


class TombTests(unittest.TestCase):
    def test_statement_example(self):
        self.assertEqual(tomb.find_path([5, 8, 12]), [5, 8, 12])

    def test_documented_backtracking_case(self):
        self.assertEqual(tomb.find_path([20, 10, 4, 7]), [20, 30, 36, 36])

    def test_single_section(self):
        self.assertEqual(tomb.find_path([5]), [5])

    def test_small_instances_against_reachability_oracle(self):
        for length in (2, 3, 4):
            for values in product(range(1, 4), repeat=length):
                with self.subTest(periods=values):
                    path = tomb.find_path(list(values), max_steps=10_000)
                    self.assertEqual(path[-1], earliest_arrival(values))
                    for i, time in enumerate(path):
                        self.assertEqual((time // values[i]) % 2, 1)
                        if i:
                            self.assertLessEqual(path[i - 1], time)
                            self.assertEqual((path[i - 1] // values[i - 1]), (time // values[i - 1]))

    def test_limit_is_an_error_not_an_impossibility_result(self):
        with self.assertRaisesRegex(ValueError, "work limit"):
            tomb.find_path([5, 8, 12], max_steps=1)


class InterfaceTests(unittest.TestCase):
    def test_imports_do_not_fetch_data_or_print(self):
        with patch("input_data.urlopen", side_effect=AssertionError("Unexpected network request")), \
                patch("builtins.print", side_effect=AssertionError("Unexpected output")):
            for module in (ranking, hiking, tomb):
                importlib.reload(module)

    def test_invalid_input(self):
        for text in ("", "0", "2\n5", "1\n0"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                tomb.parse_input(text)
        for text in ("", "0", "2\n1 3", "1\n5 2"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                hiking.parse_input(text)

    def test_readme_commands(self):
        cases = [("Aufgabe2.py", "schwierigkeiten.txt", "A C D E"),
                 ("Aufgabe3.py", "wandern.txt", "Members covered: 6/6"),
                 ("Aufgabe5.py", "grabmal.txt", "Arrival time: 12 minutes")]
        for script, fixture, expected in cases:
            with self.subTest(script=script):
                result = subprocess.run([sys.executable, script, f"examples/{fixture}"], cwd=ROOT,
                                        capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(expected, result.stdout)
                missing = subprocess.run([sys.executable, script, "missing-input.txt"], cwd=ROOT,
                                         capture_output=True, text=True, timeout=10)
                self.assertEqual(missing.returncode, 2)
                self.assertNotIn("Traceback", missing.stderr)


if __name__ == "__main__":
    unittest.main()
