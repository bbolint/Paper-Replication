## Input data: (with download link)
# - `data/raw/soc-sign-epinions.txt`: https://snap.stanford.edu/data/soc-sign-epinions.txt.gz
# - `data/raw/soc-sign-Slashdot090221.txt`: https://snap.stanford.edu/data/soc-sign-Slashdot090221.txt.gz
# - `data/raw/wiki-vote.txt`: http://konect.cc/files/download.tsv.elec.tar.bz2
#
## Output data:
# - `epinions_edge.csv`
# - `Slashdot_edge.csv`
# - `wikivote_edge.csv`


# GOAL: To import raw network data and produce edgelist csv files in the uniform format.

ROOTPATH = os.getcwd()[:-3]

if __name__ == "__main__":

    epinions = pd.read_csv(ROOTPATH + "data/raw/soc-sign-epinions.txt", header=None,
                           sep="\t", skiprows=[*range(4)], names=["from","to","sign"])
    slashdot = pd.read_csv(ROOTPATH + "data/raw/soc-sign-Slashdot090221.txt", header=None,
                            sep="\t", skiprows=[*range(4)], names=["from","to","sign"])
    wikivote = pd.read_csv(ROOTPATH + "data/raw/out.elec", header=None,
                           sep="\t", skiprows=[*range(2)], names=["from","to","sign","timestamp"])

    # wiki-vote has one additional column (unix timestamp)

    epinions.to_csv(ROOTPATH + "data/preprocessed/epinions_edges.csv", index=False)
    slashdot.to_csv(ROOTPATH + "data/preprocessed/slashdot_edges.csv", index=False)
    wikivote.to_csv(ROOTPATH + "data/preprocessed/wikivote_edges.csv", index=False)
