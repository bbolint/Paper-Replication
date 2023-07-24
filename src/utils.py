from typing import Dict, Union
import networkx as nx
import pandas as pd

import os

DATASET_EPINIONS = "epinions"
DATASET_SLASHDOT = "slashdot"
DATASET_WIKIPEDIA = "wikipedia"

def read_edgelist(
        name: str,
        shuffled: bool = False,
        path: Dict[str, None] = None) -> pd.DataFrame:
    """Read edgelist from .csv file.

    Args:
        name (str): Name of dataset that should be read
            (valid options are stored in the respective DATASET_* variables)
        shuffled (bool): Whether the shuffled version should be returned.
            Overwritten by path if it is different from None. Defaults to False.
        path (Dict[str, None], optional): Path to the respective file.
            If None, try to find it in ../data/(preprocessed|permutation)
            (relative from script execution). Defaults to None.

    Returns:
        pd.DataFrame: The edgelist as DataFrame
    """
    assert name in [DATASET_EPINIONS, DATASET_SLASHDOT, DATASET_WIKIPEDIA]

    if path is None:
        path = os.path.join(
            os.getcwd(), "..", "data", "preprocessed" if not shuffled else "permutations")
    df = pd.read_csv(os.path.join(path, f"{name}_edges.csv"))
    df = df[df["from"]!=df["to"]]  # filter out self-loops
    return df

def read_network(
        name: str,
        shuffled: bool = False,
        path: Dict[str, None] = None,
        directed: bool = True) -> Union[nx.Graph, nx.DiGraph]:
    """Read a  network object from an edgelist stored as a .csv file.

    Args:
        name (str): Name of the dataset (valid options are stored in the
            respective DATASET_* variables)
        shuffled (bool): Whether the shuffled version should be returned.
            Overwritten by path if it is different from None. Defaults to False.
        path (Dict[str, None], optional): Path to the .csv edgelist. Defaults to None.
        directed (bool, optional): Whether the returned graph should be directed or not.
            If None, try to find it in ../data/(preprocessed|permutation)
            (relative from script execution). Defaults to True.

    Returns:
        Union[nx.Graph, nx.DiGraph]: The graph restored from the edgelist.
            Directed if specified by the respective argument.
    """
    return create_network(
        edgelist=read_edgelist(name=name, shuffled=shuffled, path=path),
        directed=directed
    )

def create_network(
        edgelist: pd.DataFrame,
        directed: bool = True) -> Union[nx.Graph, nx.DiGraph]:
    """Create a network from an pandas.DataFrame edgelist.

    Args:
        edgelist (pd.DataFrame): The edgelist.
            Columns 'from' and 'to' are expected to be present in the DataFrame.
        directed (bool, optional): Whether the resulting graph is directed or not. Defaults to True.

    Returns:
        Union[nx.Graph, nx.DiGraph]: The graph object.
            Directed if specified by the respective argument.
    """
    g = nx.Graph() if not directed else nx.DiGraph()
    if "timestamp" in edgelist.columns:
        g.add_edges_from([(x["from"], x["to"], {"sign": x["sign"], "timestamp": x["timestamp"]}) for _, x in edgelist.iterrows()])
    else:
        g.add_edges_from([(x["from"], x["to"], {"sign": x["sign"]}) for _, x in edgelist.iterrows()])
    return g