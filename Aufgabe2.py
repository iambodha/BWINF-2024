"""Task 2: order selected tasks using their rankings in previous exams."""
import argparse
import heapq
from collections import defaultdict
from input_data import read_text

def read_input(file_path):
    lines = [line.strip() for line in read_text(file_path).splitlines() if line.strip()]
    if not lines:
        raise ValueError("Input is empty.")
    n, m, k = map(int, lines[0].split())
    if min(n, m, k) < 1 or k > m or len(lines) != n + 2:
        raise ValueError("Expected n exam lines and one line of k selected tasks.")
    inequalities = []
    selected_tasks = set(lines[-1].split())
    if len(selected_tasks) != k or len(lines[-1].split()) != k:
        raise ValueError("Selected task count must match k, without duplicates.")
    for i in range(1, n + 1):
        tokens = lines[i].split("<")
        if any(not token.strip() or len(token.split()) != 1 for token in tokens):
            raise ValueError("Each exam must be one ranking with '<' between task names.")
        tokens = [token.strip() for token in tokens]
        # Project the whole ranking before adding edges: A < X < B implies A < B.
        tasks = [t for t in tokens if t in selected_tasks]
        for u, v in zip(tasks, tasks[1:]):
            inequalities.append((u, v))
    return inequalities, selected_tasks

def build_graph(inequalities, selected_tasks):
    graph = defaultdict(set)
    in_degree = defaultdict(int)
    for task in selected_tasks:
        in_degree[task] = 0
    for u, v in inequalities:
        if v not in graph[u]:
            graph[u].add(v)
            in_degree[v] += 1
    return graph, in_degree

def topological_sort(graph, in_degree, selected_tasks):
    in_degree = in_degree.copy()
    queue = [node for node in selected_tasks if in_degree[node] == 0]
    heapq.heapify(queue)
    sorted_order = []
    while queue:
        node = heapq.heappop(queue)
        sorted_order.append(node)
        for neighbour in graph.get(node, []):
            in_degree[neighbour] -= 1
            if in_degree[neighbour] == 0:
                heapq.heappush(queue, neighbour)
    if len(sorted_order) != len(selected_tasks):
        return None  # detected cycle
    return sorted_order

def find_good_ordering(file_path):
    inequalities, selected_tasks = read_input(file_path)
    graph, in_degree = build_graph(inequalities, selected_tasks)
    ordering = topological_sort(graph, in_degree, selected_tasks)
    if ordering:
        return ' '.join(ordering)
    else:
        return "NO GOOD ORDERING POSSIBLE"

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", help="Input file paths or explicit HTTP(S) URLs")
    args = parser.parse_args()
    try:
        for source in args.inputs:
            print(f"{source}:\n{find_good_ordering(source)}\n")
    except (OSError, ValueError) as error:
        parser.exit(2, f"Error: {error}\n")


if __name__ == "__main__":
    main()
