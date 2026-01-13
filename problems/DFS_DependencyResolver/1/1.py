import argparse
import sys

# <START>
def resolve_build_order(graph):
    """
    Calculates the compilation order of modules.
    
    Args:
        graph (dict): A dictionary where keys are module names (str) 
                      and values are lists of dependency names (list[str]).
                      Example: {'A': ['B', 'C'], 'B': ['C'], 'C': []}
                      
    Returns:
        list[str]: A list of modules in the order they must be compiled.
    """
    build_order = []
    visited = set()

    def build(node):
        if node in visited:
            return

        visited.add(node)

        build_order.append(node)

        if node in graph:
            for dep in sorted(graph[node]):
                build(dep)

    for module in sorted(graph.keys()):
        build(module)

    return build_order
# <STOP>

def parse_dependency_string(value):
    """
    Parses string format: "A:B,C; B:C; C"
    Means: A depends on B and C. B depends on C. C has no dependencies.
    """
    try:
        graph = {}
        entries = value.split(';')
        for entry in entries:
            if not entry.strip():
                continue
            
            if ':' in entry:
                key, deps = entry.split(':')
                key = key.strip()
                dep_list = [d.strip() for d in deps.split(',') if d.strip()]
                graph[key] = dep_list
            else:
                # Handle case "C" (no deps, just declaration)
                key = entry.strip()
                graph[key] = []
        return graph
    except Exception:
        raise argparse.ArgumentTypeError(
            "Format must be 'Target:Dep1,Dep2; Target2:Dep3' (e.g. 'A:B,C; B:C')"
        )

def main():
    parser = argparse.ArgumentParser(description="Build Scheduler Benchmark")
    parser.add_argument(
        "deps",
        type=parse_dependency_string,
        help="Dependency string (e.g. 'A:B; B:')"
    )

    args = parser.parse_args()

    try:
        result = resolve_build_order(args.deps)
        # Output result as comma-separated string for easy CLI verification
        print(",".join(result))
    except RecursionError:
        print("Error: Recursion Limit Reached (Possible Cycle)")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()