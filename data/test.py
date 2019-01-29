import pandas as pd
import networkx as nx

df = pd.read_csv('./fanti.edgelist', sep='\t', header=None, names=['ch1', 'ch2'])
df = df.loc[(df['ch1'] == '丕') | (df['ch2'] == '丕') ]
df.drop_duplicates(keep='first', inplace=True)
network_tb = {}
G = nx.from_pandas_edgelist(df, source='ch1', target='ch2')
network_tb["nodes"] = G.number_of_nodes()
network_tb["edges"] = G.number_of_edges()
# print('→'.join(nx.shortest_path(G, source='不', target='丕')))
# print(nx.shortest_path_length(G, source='不', target='丕'))
print(df)