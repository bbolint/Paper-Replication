# Paper replication PhD project:
Leskovec, J., Huttenlocher, D. P. & Kleinberg, J. M. (2010). Signed networks in social media.. In E. D. Mynatt, D. Schoner, G. Fitzpatrick, S. E. Hudson, W. K. Edwards & T. Rodden (eds.), CHI (p./pp. 1361-1370), : ACM. ISBN: 978-1-60558-929-9

# My role
This repository was created as a mutual effort by multiple students in the Network Science PhD program at the Central European University.

I contributed to the project by the following code:
- src/Print Figure 2.ipynb (recreating Figure 2 of the original paper)
- src/receptive_generative_baselines.ipynb (calculate baselines for receptive and generative vertices)
- src/wikipedia_triads_sequential_edgelist.ipynb (create edgelist from Wikipedia dataset)

## Dataset
We will create networks using three datasets (stored in data/raw):
- [Epinions](https://snap.stanford.edu/data/soc-sign-epinions.html)
- [Slashdot](https://snap.stanford.edu/data/soc-sign-Slashdot090221.html)
- [Wikipedia](http://konect.cc/files/download.tsv.elec.tar.bz2)
  - (more documentation on the data is available in `README.elec`)


## Script descriptions
(please only include descriptions for crucial pipeline scripts so it'll be easier for our final clean-up stage)

### Preprocessing
- `import_clean.py`: import and clean network data, save edgelist csv files
- `utils.py`: load datasets into `pandas.DataFrame` edgelist, `networkx.Graph` or `networkx.DiGraph` object

### Analysis
- `search_triads.py`: search static triads (i.e., T0, T1, T2, T3) in networks; merge same-sign edges
- `search_triads_new.py`: search static triads (i.e., T0, T1, T2, T3) in networks; does not merge same-sign edges
- `receptive_generative_baselines`: calculates receptive and generative probabilities for negative & positive edges for epinions and wikipedia datasets
- `wikipedia_triads_sequential_edgelist`: Create dataframe with sequence of linkages within eventual triads (wikipedia)
- `shuffle_networks.ipynb`: import networks, shuffles the signs across the edges and stores the result in `data/permutations`


### Output folders
- `Recipro_stat_table4` folder contains all the files, scripts, and results related to reproducing Table. 4
- `One_sign_Net_Table6` folder contains all the files, scripts, and results related to reproducing Table. 6

### Results
- `print_table1.ipynb`: print out Table 1 -- # nodes, edges, triads
- `print_table2.ipynb`: print out Table 2 -- probabilities of (shuffled) triads, surprise
  - TODO: waiting for the counting to finish, will update Table 2 soon.
- `print_figure_3.ipynb`: compute relationship between positive links and fraction of common neighbors between the two nodes (Figure 3).
- `wikipedia_triads_statistics_table5.ipynb`: print the values of table 5. 
- `Code_one_sign_net.py`: compute statistics of only one sign networks (Table 6).
