"""
    LDFI Interpreter main program execution
"""
import argparse
import sys
import json
from graphviz import Digraph


def handle_arguments():
    """
        Method to Set CLA

        Parameters:
        None

        Returns:
        parser (ArgumentParser object)
    """
    parser = argparse.ArgumentParser(description="Take 3MileBeach trace and convert to DAG")

    parser.add_argument("-i", "--input", dest="input_file",
                        help="input json file")
    parser.add_argument("-o", "--output", dest="output_file",
                        help="output DAG graph file")

    return parser


def directed_acyclic_graph(graph, output_file):
    """
        Method used to create a directed acyclic graph

        Parameters:
        graph (dict): graph node and node neighbors relation
        output_file (string): name of the output file

        Returns:
        None
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

    dot.render(output_file, view=True)


def records_preprocessing(traces):
    """
        Method used to preprocess trace information in order to
        successfully create a DAG for a given request flow

        Parameters:
        traces (dict): Information about an individual trace

        Returns:
        node_mapping (dict): nodes and neighbors data for DAG
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
    """
        Main Entrance
    """
    parser = handle_arguments()
    args = parser.parse_args()

    if not args.input_file or not args.output_file:
        parser.print_help()
        sys.exit(1)

    input_file = open(args.input_file, "r")
    data = json.load(input_file)
    input_file.close()

    data = records_preprocessing(data)
    directed_acyclic_graph(data, args.output_file)


if __name__ == "__main__":
    main()
