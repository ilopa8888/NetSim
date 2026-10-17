 
import json
import sys
from collections import deque
from pathlib import Path


def load_topology(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def build_graph(topology):
    graph = {node: [] for node in topology["nodes"]}

    for a, b in topology["links"]:
        if a not in graph or b not in graph:
            raise ValueError(f"Unknown node in link: {a} - {b}")

        graph[a].append(b)
        graph[b].append(a)

    return graph


def find_path(graph, start, destination):
    if start not in graph or destination not in graph:
        return None

    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        node, path = queue.popleft()

        if node == destination:
            return path

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None


def main():
    filename = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "topologies/office.json"
    )

    topology = load_topology(filename)
    graph = build_graph(topology)

    print("Network nodes:")
    for node in graph:
        print(f"  {node}: {', '.join(graph[node]) or 'No connections'}")

    start = input("\nStart node: ").strip()
    destination = input("Destination node: ").strip()

    path = find_path(graph, start, destination)

    if path:
        print("\nPath found:")
        print(" -> ".join(path))
    else:
        print("\nNo path found. Check the node names and connections.")


if __name__ == "__main__":
    main()
