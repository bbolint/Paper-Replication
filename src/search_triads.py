import os
import pandas as pd
import numpy as np
import networkx as nx
from collections import defaultdict
# from networkx.algorithms.triads import all_triads, is_triad, triad_type, triadic_census
from utils import read_edgelist, read_network, DATASET_EPINIONS, DATASET_WIKIPEDIA, DATASET_SLASHDOT
from itertools import combinations
import argparse
import pickle

ROOTPATH = os.getcwd()[:-3]

# TODO: add more comments

def create_network_lite(df):
    """
    Create an undirected weighted graph from a edgelist dataframe.
    The edge weights equal to the number of unique signs between two nodes, i.e., weight = 1 if two nodes has two positive/negative edges; weight = 2 if one positive and one negative.

    Args:
        df (pd.DataFrame): the edgelist

    Returns:
        nx.Graph: an undirected weighted graph
    """
    def_weight = 1
    g = nx.Graph()
    for _, x in df.iterrows():
        if (g.has_edge(x["from"],x["to"])) and (g[x["from"]][x["to"]]["sign"]!=x["sign"]):
            g[x["from"]][x["to"]]["weight"] += 1
        else:
            g.add_edge(x["from"], x["to"], weight=def_weight, sign=x["sign"])
    return g


def sum_link_attr(triplet, g, attr):
    """
    Sum up link attributes (weights or sign) for triads categorization.

    Args:
        triplet (frozenset): a frozenset of nodes in a triad.
        g (nx.Graph): the entire graph object.
        attr (str): the name of attributes we want to sum

    Returns:
        int: the value of attribute sum
    """
    triplet = list(triplet)
    x1 = g[triplet[0]][triplet[1]][attr]
    x2 = g[triplet[0]][triplet[2]][attr]
    x3 = g[triplet[1]][triplet[2]][attr]
    return int(x1+x2+x3)


def search_triangles(g):
    """
    Search all unique triangles in an undirected graph.

    Args:
        g (nx.Graph): the graph to search on

    Returns:
        list: a list of node set for all triangles
    """
    triplets = []
    for n in g.nodes():
        for nb, nb2 in combinations(g[n],2):
            if g.has_edge(nb, nb2):
                triplets.append(frozenset((n, nb, nb2)))
    return list(set(triplets))


def search_triangles_by_type(g):
    """
    Search all unique triangles and return a dictionary of triangles by its static type (Leskovec, Huttenlocher, & Kleiberg, 2010)

    Args:

    Returns:

    """
    TRIADS = np.zeros(4)
    uniq_tris = search_triangles(g)
    for tri in uniq_tris:
        sum_weights = sum_link_attr(tri, g, "weight")
        sum_signs = sum_link_attr(tri, g, "sign")
        if sum_weights == 3:
            if sum_signs == -3:
                TRIADS[0] += 1
            elif sum_signs == -1:
                TRIADS[1] += 1
            elif sum_signs ==1:
                TRIADS[2] += 1
            else:  # sum_signs == 3:
                TRIADS[3] += 1
        elif sum_weights == 4:
            if sum_signs == -2:
                TRIADS[0] += 1
                TRIADS[1] += 1
            elif sum_signs == 0:
                TRIADS[1] += 1
                TRIADS[2] += 1
            else:  # sum_signs == 2:
                TRIADS[2] += 1
                TRIADS[3] += 1
        elif sum_weights == 5:
            if sum_signs == -1:
                TRIADS[0] += 1
                TRIADS[1] += 2
                TRIADS[2] += 1
            else:  # sum_signs == 1:
                TRIADS[1] += 1
                TRIADS[2] += 2
                TRIADS[3] += 1
        elif sum_weights == 6:
                TRIADS[0] += 1
                TRIADS[1] += 3
                TRIADS[2] += 3
                TRIADS[3] += 1
    return TRIADS


# def save_triads(triads_dict, name, shuffled=False):
#     fname = name + "_triads"
#     if shuffled:
#         fname = "shuffled_" + name + "_triads"
#     with open(ROOTPATH + f"data/preprocessed/{fname}.pkl", "wb") as file:
#         pickle.dump(triads_dict, file, protocol=pickle.HIGHEST_PROTOCOL)
#
#
# def read_triads(name, shuffled=False):
#     fname = name + "_triads"
#     if shuffled:
#         fname = "shuffled_" + name + "_triads"
#     with open(ROOTPATH + f"data/preprocessed/{fname}.pkl", "rb") as file:
#         triads = pickle.load(file)
#     return triads
#
#
# def count_triads(triads_dict):
#     n = 0
#     for t,ls in triads_dict.items():
#         n += len(ls)
#     return n


if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument("--shuffled", help="Whether to use the shuffled links or not", type=bool, default=False, required=False)
    args = argparser.parse_args()

    df_dict = {}
    df_dict["wikipedia"] = read_edgelist(DATASET_WIKIPEDIA, shuffled=args.shuffled)
    df_dict["epinions"] = read_edgelist(DATASET_EPINIONS, shuffled=args.shuffled)
    df_dict["slashdot"] = read_edgelist(DATASET_SLASHDOT, shuffled=args.shuffled)

    output_df = pd.DataFrame()
    output_df["triads"] = ["T0", "T1", "T2", "T3"]
    for name,df in df_dict.items():
        print(f"Searching triads on {name} network...")
        glite = create_network_lite(df)
        triads = search_triangles_by_type(glite)
        print("Results:", triads)
        output_df[name] = triads

    new_file = "static_triads1"
    if args.shuffled:
        new_file = new_file + "_shuffled"
    output_df.to_csv(ROOTPATH + f"data/summary/{new_file}.csv", index=False)
