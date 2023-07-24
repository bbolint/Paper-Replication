import numpy as np
import pandas as pd
import networkx as nx

Datasets = ['epinions','slashdot','wikipedia']

node_number = []
#### Create Shuffled Network ###################
for data in Datasets:
    df = pd.read_csv(data+'_edges.csv',delimiter=',')
    signs_shuffled = np.random.permutation(df["sign"])
    df_copy = df.copy()
    df_copy["sign"] = signs_shuffled
    df_copy.to_csv(data+'_shuffled_edges.csv',index = False)

    g = nx.Graph()
    edgelist = [(x["from"], x["to"]) for i,x in df_copy.iterrows()]
    g.add_edges_from(edgelist)

    node_number.append(len(g.nodes()))
################################################

print(node_number)

file = open("One_sign_net.txt", "w")

##### Creating the signed Network ##########################
def signed_net(Original_df: pd.DataFrame,sign_value,normalization,sign_text):
    sub_df = Original_df.loc[ Original_df['sign'] == sign_value]

    L = set(sub_df['from']) | set(sub_df['to'])
    L = np.sort( list(L) )
    d = {v: i for i, v in enumerate(L)}

    def relabel(value):
        ind = d[value]
        return ind

    sub_df.loc[:, 'from'] = sub_df['from'].map(relabel)
    sub_df.loc[:, 'to'] = sub_df['to'].map(relabel)

    sub_df.to_csv(sign_text+'.csv', index = False)

    g = nx.Graph()
    edgelist = [(x["from"], x["to"]) for i,x in sub_df.iterrows()]
    g.add_edges_from(edgelist)

    tri = nx.transitivity(g)
    gcc = len(max(nx.connected_components(g), key=len))

    file.write(sign_text+' edges = '+str(len(sub_df))+'\n')
    file.write(sign_text+' Clustering = '+str(round(tri,3))+'\n')
    file.write(sign_text+' gcc = '+ str(round(gcc/normalization,3))+'\n')


for data,nn in zip(Datasets,node_number):

    df = pd.read_csv(data+'_edges.csv',delimiter=',')
    signed_net(df,-1,nn,data+'_negative_edges')
    signed_net(df,1,nn,data+'_positive_edges')

    df = pd.read_csv(data+'_shuffled_edges.csv',delimiter=',')
    signed_net(df,-1,nn,data+'_shuffled_positive_edges')
    signed_net(df,1,nn,data+'_shuffled_negative_edges')

    print(data+' is done.')
#####################################################

file.close()