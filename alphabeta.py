import re
import math


class Node:
    def __init__(self, name, children, maxplayer, isTerminal):
        self.name = name
        self.children = children
        self.maximizingPlayer = maxplayer
        self.isTerminal = isTerminal


# Reading information from file
alphabeta_data = open("alphabeta.txt", "r")
lines = []
for line in alphabeta_data:
    lines.append(line)

# List of all problems
problems = []

# Create node lists for each problem
for line in lines:
    data = line.split()
    # Remove curly braces
    data[0] = data[0].replace("{", "")
    data[0] = data[0].replace("}", "")
    data[1] = data[1].replace("{", "")
    data[1] = data[1].replace("}", "")

    # Get list of all node player types (max/min)
    playerTypes = re.findall('\(.*?\)', data[0])
    paircount = len(playerTypes)
    for i in range(paircount):
        playerTypes[i] = playerTypes[i].replace("(", "")
        playerTypes[i] = playerTypes[i].replace(")", "")
        playerTypes[i] = playerTypes[i].split(',')

    # Get list of all node connections
    connections = re.findall('\(.*?\)', data[1])
    paircount = len(connections)
    for i in range(paircount):
        connections[i] = connections[i].replace("(", "")
        connections[i] = connections[i].replace(")", "")
        connections[i] = connections[i].split(',')

    # Build list of nodes
    nodes = []
    for entry in playerTypes:
        name = entry[0]
        type = entry[1]
        # Label as either maxplayer or miniplayer
        if entry[1] == 'MAX':
            maxplayer = True
        else:
            maxplayer = False
        # Create the node
        node = Node(name, [], maxplayer, False)
        nodes.append(node)
    # Build the nodes' lists of children from the provided connections
    for entry in connections:
        parent = entry[0]
        child = entry[1]
        # Check if child is a leaf and handle accordingly
        if child.isdigit():
            child = int(child)
            node = Node(child, None, None, True)
            nodes.append(node)
        # Find parent node in list and add the child to its list of children
        for parent_node in nodes:
            if parent_node.name == parent:
                # parent node found
                for child_node in nodes:
                    if child_node.name == child:
                        parent_node.children.append(child_node)

    # add list of nodes to list of problems
    problems.append(nodes)


# Minimax algo

def alphabeta(node, alpha, beta, maximizingPlayer, isTerminal):
    if isTerminal:
        # current node is a leaf => update counter of leaves examined and return leaf value
        global leaves_examined
        leaves_examined = leaves_examined + 1
        return node.name
    if maximizingPlayer:
        value = -math.inf
        for child in node.children:
            value = max(value, alphabeta(
                child, alpha, beta, False, child.isTerminal))
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # beta cut
        return value
    else:
        value = math.inf
        for child in node.children:
            value = min(value, alphabeta(
                child, alpha, beta, True, child.isTerminal))
            beta = min(beta, value)
            if alpha >= beta:
                break  # alpha cut
        return value


# Format output file
graph_count = 1
output = []
for problem in problems:
    leaves_examined = 0
    results = alphabeta(problem[0], -math.inf, math.inf, True, False)
    string = "Graph " + str(graph_count) + ": Score: " + str(results) + \
        "; Leaf Nodes Examined: " + str(leaves_examined)
    output.append(string)
    graph_count += 1

# Write output to file
out_file = open("alphabeta_out.txt", "w")
for graph in output:
    out_file.write(graph)
    out_file.write("\r\n\n")
