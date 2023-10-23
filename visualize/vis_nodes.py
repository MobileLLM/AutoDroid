import json
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

PATH = "state_2023-10-20_134316.json"
G = nx.DiGraph()
with open(PATH, "r") as f:
    data = json.load(f)
nodes = data["views"]

for node in nodes:
    title = {
        "text": node["text"],
        "clickable": node["clickable"],
        "class": node["content_description"],
        "scrollable": node["scrollable"],
        "visible": node["visible"]
    }
    color = "#00ccff"
    if node["text"] and node["clickable"]:
        color = "#ff00ff"
    if node["text"] and not node["clickable"]:
        color = "#ff0000"
    if not node["text"] and node["clickable"]:
        color = "#33cc33"
    if node["scrollable"]:
        color = "#808080"
    G.add_node(node["temp_id"], title=str(title), label=str(node["temp_id"]), color=color)  

for node in nodes:
    idx = node["temp_id"]
    parent = node["parent"]
    children = node["children"]
    if not G.has_edge(parent, idx) and parent != -1:
        G.add_edge(parent, idx)
    for child in children:
        if not G.has_edge(idx, child):
            G.add_edge(idx, child)

nt = Network('1500px', notebook=True, directed=True)
nt.from_nx(G)
nt.toggle_physics(True)
nt.show('nx.html')
