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
    
    # State tracking for Cycle Detection
    # 0 = Unvisited
    # 1 = Visiting (Currently in recursion stack - Gray)
    # 2 = Visited (Fully processed - Black)
    state = {}

    def visit(node):
        current_state = state.get(node, 0)
        
        # CYCLE DETECTED: We ran into a node that is currently being visited
        if current_state == 1:
            raise ValueError(f"Circular dependency detected involving '{node}'")
        
        # ALREADY PROCESSED: Skip to avoid duplicates
        if current_state == 2:
            return

        # MARK AS VISITING (Gray)
        state[node] = 1

        # GET DEPENDENCIES
        # Use .get() to handle implicit leaf nodes (nodes that are deps but not keys)
        dependencies = graph.get(node, [])
        
        # Sort dependencies to ensure deterministic output (crucial for benchmarking)
        for dep in sorted(dependencies):
            visit(dep)

        # MARK AS VISITED (Black)
        state[node] = 2
        
        # POST-ORDER APPEND: Add to list only AFTER dependencies are done
        build_order.append(node)

    # 1. Identify all unique nodes (keys + all values) to handle disconnected graphs
    #    and implicit leaf nodes properly.
    all_nodes = set(graph.keys())
    for deps in graph.values():
        all_nodes.update(deps)

    # 2. Iterate through all nodes (sorted for deterministic starting points)
    for node in sorted(all_nodes):
        visit(node)

    return build_order
# <STOP>

def parse_dependency_string(value):
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
                key = entry.strip()
                graph[key] = []
        return graph
    except Exception:
        raise argparse.ArgumentTypeError("Invalid format")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("deps", type=parse_dependency_string)
    args = parser.parse_args()

    try:
        result = resolve_build_order(args.deps)
        print(",".join(result))
    except ValueError as e:
        print(f"Error: {e}")
    except RecursionError:
        print("Error: Recursion Limit Reached")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()