import sys
import networkx as nx
from ordered_set import OrderedSet

MAPPING = {}

def read_pairs(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    pairs = []
    for idx, line in enumerate(lines):
        try:
            parent, child = line.split('->')
            parent = parent.strip()
            MAPPING[parent.lower()] = parent
            child = child.strip()
            MAPPING[child.lower()] = child
            pairs.append((parent.lower(), child.lower(), 1))
        except Exception as e:
            raise ValueError(f'Error parsing line {idx}')
    return pairs

def read_selections(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    selections = []
    for line in lines:
        selection = line.strip()
        MAPPING[selection.lower()] = selection
        selections.append(selection.lower())
    return selections

def main():
    pairs_filename = sys.argv[1]
    selections_filename = sys.argv[2]
    pairs = read_pairs(pairs_filename)
    selections = read_selections(selections_filename)
    dg = nx.DiGraph()
    dg.add_weighted_edges_from(pairs)
    connectivity = nx.all_pairs_node_connectivity(dg)
    results = OrderedSet()
    for k, v in connectivity.items():
        if k in selections:
            results.add(MAPPING[k])
            for k2, v2 in v.items():
                if v2:
                    results.add(MAPPING[k2])
    for r in results:
        print(r)

if __name__ == '__main__':
    main()