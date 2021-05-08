"""
    LDFI Interpreter main program execution
"""
import argparse
import sys
import json
import copy
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
    parser.add_argument("-l", "--lineage", dest="lineage", action="store_true")

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


def records_lineage_preprocessing(traces):
    """
        Method used to preprocess trace information in order to
        successfully create lineage between requests

        Parameters:
        traces (dict): Information about an individual trace

        Returns:
    """
    trace_flows = {}
    flows = []
    services = set()


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

    # 3. Combine Send - Receive pairs
    for key in trace_flows:
        data = trace_flows[key]

        if len(data) > 2:
            flows.append(data[:2])
            flows.append(data[len(data) - 2 :len(data)])
        elif len(data) == 2:
            flows.append(data[:2])

    # 4. Sort Send - Receive pairs by timestamp
    flows.sort(key=lambda x: x[0]["timestamp"])

    # 5. Get all unique services
    for flow in flows:
        for record in flow:
            services.add(record["service"])

    return flows, list(services)


class Lineage:
    def __init__(self):
        self.nodes = []
        self.dot = None
        self.services = []

    def create_lineage_graph(self, data, services):
        self.nodes = []
        self.data = data
        self.services = services
        self.dot = Digraph(comment="Lineage Graph", format="png")
        service_clocks = {}

        for service in self.services:
            service_clocks[service] = 0

        self.lineage_helper("client-1769190683", service_clocks, 0)
        self.dot.render("test-output", view=True)

    def lineage_helper(self, curr_service, service_clocks, index):
        curr_sender = None
        i = index

        while i < len(self.data):
            sender, receiver = self.data[i]

            if curr_service == sender["service"]:
                self.data.pop(i)
                s_service = sender["service"]
                r_service = receiver["service"]

                if not curr_sender:
                    s_str = f"{s_service}_{service_clocks[s_service]}"
                    curr_sender = s_str
                else:
                    s_str = curr_sender

                r_str = f"{r_service}_{service_clocks[r_service]}"

                if s_str not in self.nodes:
                    self.nodes.append(s_str)
                    self.dot.node(s_str, label=s_str)
                if r_str not in self.nodes:
                    self.nodes.append(r_str)
                    self.dot.node(r_str, label=r_str)

                self.dot.edge(s_str, r_str, label=sender["message_name"])

                service_clocks[sender["service"]] += 1

                curr = receiver["service"]
                self.lineage_helper(curr, service_clocks, i)
            else:
                i += 1


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

    if args.lineage:
        # Create Lineage Graph
        print("Creating Lineage Graph")
        data, services = records_lineage_preprocessing(data)

        # User Data and unique services to create Graph of lineage
        lin = Lineage()
        lin.create_lineage_graph(data, services)
    else:
        # Create Call Gaph
        data = records_preprocessing(data)
        directed_acyclic_graph(data, args.output_file)


if __name__ == "__main__":
    main()
