"""
    LDFI Interpreter main program execution
"""
import json
from graphviz import Digraph


def directed_acyclic_graph(graph):
    """
        Method used to create a directed acyclic graph
    """
    dot = Digraph(comment="Test Home Request", format="png")
    nodes = []

    for key in graph:
        if key not in nodes:
            nodes.append(key)
            dot.node(key, label=key)

        neighbors = graph[key]

        for neighbor in neighbors:
            if neighbor not in nodes:
                nodes.append(neighbor)
                dot.node(neighbor, label=neighbor)

            dot.edge(key, neighbor)

    dot.render("dag.gv", view=True)


def records_preprocessing(traces):
    """
    """
    trace_flows = {}
    new_flows = {}
    node_mapping = {}

    # 1. aggregate requests and responses by uuid
    for record in traces["records"]:
        try:
            trace_flows[record["uuid"]].append(record)
        except KeyError:
            trace_flows[record["uuid"]] = []
            trace_flows[record["uuid"]].append(record)

    # 2. Sort request response flows
    for key in trace_flows:
        data = trace_flows[key]
        data.sort(key=lambda x: x["timestamp"])
        trace_flows[key] = data

    # 3. Prune responses
    for key in trace_flows:
        data = trace_flows[key]
        data = data[:2]
        trace_flows[key] = data

    # 4. Prune failed requests and combine all records
    for key in trace_flows:
        data = trace_flows[key]

        if len(data) == 2:
            new_flows[key] = data

    # 5. Node to neighbors processing
    for key in new_flows:
        data = new_flows[key]

        node = data[0]
        neighbor = data[1]
        try:
            node_mapping[node["service"]].append(neighbor["service"])
        except KeyError:
            node_mapping[node["service"]] = []
            node_mapping[node["service"]].append(neighbor["service"])

    # 6. Make sure all neighbors are unique
    for key in node_mapping:
        node_mapping[key] = list(set(node_mapping[key]))

    return node_mapping


def main():
    test_file = open("./testoutput.json", "r")
    data = json.load(test_file)
    test_file.close()

    data = records_preprocessing(data)
    print(data)

    directed_acyclic_graph(data)

    """
    out_file = open("./out.json", "w+")
    out_file.write(json.dumps(data, indent=4, sort_keys=True))
    out_file.close()
    """


if __name__ == "__main__":
    main()