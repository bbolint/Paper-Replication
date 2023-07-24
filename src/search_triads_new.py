import os
import pandas as pd
import numpy as np
import networkx as nx
from collections import defaultdict
# from networkx.algorithms.triads import all_triads, is_triad, triad_type, triadic_census
from utils import read_edgelist, read_network, create_network, DATASET_EPINIONS, DATASET_WIKIPEDIA, DATASET_SLASHDOT
from itertools import combinations
import argparse
import pickle

ROOTPATH = os.getcwd()[:-3]


def create_network_weighted(df):
    g = nx.Graph()
    for _, x in df.iterrows():
        if (g.has_edge(x["from"],x["to"])):
            g[x["from"]][x["to"]]["weight"] += 1
        else:
            g.add_edge(x["from"], x["to"], weight=1)
    return g


def search_triangles(g):
    triplets = []
    for n in g.nodes():
        for nb, nb2 in combinations(g[n],2):
            if g.has_edge(nb, nb2):
                triplets.append(frozenset((n, nb, nb2)))
    return list(set(triplets))


def sum_link_sign(srcs, tars, df):
    x = 0
    for s,t in zip(srcs, tars):
        x += df[(df["from"]==s)&(df["to"]==t)]["sign"].values[0]
    return x


def return_triad_type(srcs, tars, df):
    all_t = np.zeros(4)
    if sum_link_sign(srcs, tars, df) == 3:
        all_t[3] += 1
    elif sum_link_sign(srcs, tars, df) == 1:
        all_t[2] += 1
    elif sum_link_sign(srcs, tars, df) == -1:
        all_t[1] += 1
    elif sum_link_sign(srcs, tars, df) == -3:
        all_t[0] += 1
    return all_t


def count_triads(triplet, g_directed, df):
    triplet = list(triplet)
    TRIADS = []
    # 8 possible motifs
    # 1. a->b, a->c, b->c
    if (g_directed.has_edge(triplet[0],triplet[1])) and (g_directed.has_edge(triplet[0],triplet[2])) \
    and (g_directed.has_edge(triplet[1],triplet[2])):
        TRIADS.append(return_triad_type([triplet[0],triplet[0],triplet[1]],
                                        [triplet[1],triplet[2],triplet[2]], df))
    # 2. a->b, a->c, b<-c
    if (g_directed.has_edge(triplet[0],triplet[1])) and (g_directed.has_edge(triplet[0],triplet[2])) \
    and (g_directed.has_edge(triplet[2],triplet[1])):
        TRIADS.append(return_triad_type([triplet[0],triplet[0],triplet[2]],
                                        [triplet[1],triplet[2],triplet[1]], df))
    # 3. a->b, a<-c, b->c
    if (g_directed.has_edge(triplet[0],triplet[1])) and (g_directed.has_edge(triplet[2],triplet[0])) \
    and (g_directed.has_edge(triplet[1],triplet[2])):
        TRIADS.append(return_triad_type([triplet[0],triplet[2],triplet[1]],
                                        [triplet[1],triplet[0],triplet[2]], df))
    # 4. a->b, a<-c, b<-c
    if (g_directed.has_edge(triplet[0],triplet[1])) and (g_directed.has_edge(triplet[2],triplet[0])) \
    and (g_directed.has_edge(triplet[2],triplet[1])):
        TRIADS.append(return_triad_type([triplet[0],triplet[2],triplet[2]],
                                        [triplet[1],triplet[0],triplet[1]], df))
    # 5. a<-b, a->c, b->c
    if (g_directed.has_edge(triplet[1],triplet[0])) and (g_directed.has_edge(triplet[0],triplet[2])) \
    and (g_directed.has_edge(triplet[1],triplet[2])):
        TRIADS.append(return_triad_type([triplet[1],triplet[0],triplet[1]],
                                        [triplet[0],triplet[2],triplet[2]], df))
    # 6. a<-b, a->c, b<-c
    if (g_directed.has_edge(triplet[1],triplet[0])) and (g_directed.has_edge(triplet[0],triplet[2])) \
    and (g_directed.has_edge(triplet[2],triplet[1])):
        TRIADS.append(return_triad_type([triplet[1],triplet[0],triplet[2]],
                                        [triplet[0],triplet[2],triplet[1]], df))
    # 7. a<-b, a<-c, b->c
    if (g_directed.has_edge(triplet[1],triplet[0])) and (g_directed.has_edge(triplet[2],triplet[0])) \
    and (g_directed.has_edge(triplet[1],triplet[2])):
        TRIADS.append(return_triad_type([triplet[1],triplet[2],triplet[1]],
                                        [triplet[0],triplet[0],triplet[2]], df))
    # 8. a<-b, a<-c, b<-c
    if (g_directed.has_edge(triplet[1],triplet[0])) and (g_directed.has_edge(triplet[2],triplet[0])) \
    and (g_directed.has_edge(triplet[2],triplet[1])):
        TRIADS.append(return_triad_type([triplet[1],triplet[2],triplet[2]],
                                        [triplet[0],triplet[0],triplet[1]], df))
    return TRIADS



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
        print(f"Counting triads on {name} network...")
        g_directed = create_network(df, directed=True)
        g_weighted = create_network_weighted(df)
        triads = search_triangles(g_weighted)
        ALL_TRIADS = []
        for i,t in enumerate(triads):
            if i%2000==0: print("  progress:", i/len(triads))
            ALL_TRIADS.append(np.sum(count_triads(t, g_directed, df), axis=0))
        ALL_TRIADS = np.sum(ALL_TRIADS, axis=0)
        print("Results:", ALL_TRIADS)
        output_df[name] = ALL_TRIADS

    new_file = "static_triads2"
    if args.shuffled:
        new_file = new_file + "_shuffled"
    output_df.to_csv(ROOTPATH + f"data/summary/{new_file}.csv", index=False)
