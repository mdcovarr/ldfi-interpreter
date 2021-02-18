"""
    LDFI Interpreter main program execution
"""
import json
from graphviz import Digraph


def directed_acyclic_graph_bfs(starting, edges):
    """
        Function to generate a directed acyclic graph
        with the help of breadth first search algorithm

        procedure BFS(G, root) is
            let Q be a queue
            label root as discovered
            Q.enqueue(root)
            while Q is not empty do
                v := Q.dequeue()
                if v is the goal then
                    return v
                for all edges from v to w in G.adjacentEdges(v) do
                    if w is not labeled as discovered then
                        label w as discovered
                        Q.enqueue(w)

        Parameters:
        starting (str): name of the starting location node
        edges (list): list of edges that we would like to traverse

        Returns:

    """
    queue = []
    nodes = []
    # Need to mark starting as discovered
    dot = Digraph(comment="Test Home Request")
    dot.node(starting, label=starting)
    nodes.append(starting)

    # Add edges that starting adds requests to
    i = 0
    while i < len(edges):
        edge = edges[i]

        if starting == edge["service"] and edge["type"] == 1:
            queue.append(edges.pop(i))
        else:
            i += 1

    # now we need to determine name of service that
    # is receiving the sent request
    while len(queue) > 0:
        req = queue.pop(0)

        # looking for the corresponding response
        i = 0
        edge = None
        while i < len(edges):
            edge = edges[i]
            if req["uuid"] == edge["uuid"] and edge["type"] == 2:
                edge = edges.pop(i)
                break
                queue.append(edges.pop(i))
                if edge["service"] not in nodes:
                    dot.node(edge["service"], label=edge["service"])
                    nodes.append(edge["service"])
                    # Need to add edges
                    dot.edge(req["service"], edge["service"])
            else:
                i += 1


        # if node not in nodes list, then add
        if edge["service"] not in nodes:
            dot.node(edge["service"], label=edge["service"])
            nodes.append(edge["service"])

        # Now add all edges that current node is communicating too
        node = edge["service"]
        i = 0
        while i < len(edges):
            edge = edges[i]
            if node == edge["sevice"] and edge["type"] == 1:
                pass



        break



    print(queue)
    print(nodes)
    print(dot.source)


def combine_by_uuid(traces):
    """
    """
    trace_flows = {}

    for record in traces["records"]:
        try:
            trace_flows[record["uuid"]].append(record)
        except KeyError:
            trace_flows[record["uuid"]] = []
            trace_flows[record["uuid"]].append(record)

    for key in trace_flows:
        data = trace_flows[key]
        data.sort(key=lambda x: x["timestamp"])
        trace_flows[key] = data

    traces["records"] = trace_flows
    return traces


def main():
    test_file = open("./testoutput.json", "r")
    data = json.load(test_file)
    out_file = open("./out.json", "w+")
    out_file.write(json.dumps(data, indent=4, sort_keys=True))
    out_file.close()

    input_file = open("./out.json", "r")
    data = json.load(input_file)

    data = combine_by_uuid(data)


if __name__ == "__main__":
    main()