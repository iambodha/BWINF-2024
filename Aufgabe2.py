from collections import defaultdict, deque

def read_input(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]
    n, m, k = map(int, lines[0].split())
    inequalities = []
    selected_tasks = set(lines[-1].split())
    for i in range(1, n + 1):
        tokens = lines[i].replace(';', '').replace(',', '').split()
        tasks = [t for t in tokens if t != '<']
        for u, v in zip(tasks, tasks[1:]):
            if u in selected_tasks and v in selected_tasks:
                inequalities.append((u, v))
    return inequalities, selected_tasks

def build_graph(inequalities, selected_tasks):
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    for task in selected_tasks:
        in_degree[task] = 0
    for u, v in inequalities:
        graph[u].append(v)
        in_degree[v] += 1
    for node in graph:
        graph[node] = sorted(graph[node])
    return graph, in_degree

def topological_sort(graph, in_degree, selected_tasks):
    queue = deque(sorted([node for node in selected_tasks if in_degree[node] == 0]))
    sorted_order = []
    while queue:
        node = queue.popleft()
        sorted_order.append(node)
        for neighbour in graph.get(node, []):
            in_degree[neighbour] -= 1
            if in_degree[neighbour] == 0:
                queue.append(neighbour)
        queue = deque(sorted(queue))
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

if __name__ == "__main__":
    file_paths = [
        "schwierigkeiten0.txt",
        "schwierigkeiten1.txt",
        "schwierigkeiten2.txt",
        "schwierigkeiten3.txt",
        "schwierigkeiten4.txt",
        "schwierigkeiten5.txt",
    ]
    for file_path in file_paths:
        result = find_good_ordering(file_path)
        print(f"{file_path}:\n{result}\n")

