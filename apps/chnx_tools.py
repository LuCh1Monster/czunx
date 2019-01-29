import networkx as nx
import pandas as pd
from networkx.exception import NetworkXNoPath, NodeNotFound
from pyecharts import Graph
from czunx.settings import DATA_URL


def jsnx(ch1, ch2):
    df = pd.read_csv(DATA_URL + '/fanti.edgelist', sep='\t', header=None, names=['ch1', 'ch2'])
    df.drop_duplicates(keep='first', inplace=True)
    df = df.loc[(df['ch1'] == ch1) | (df['ch2'] == ch1) | (df['ch1'] == ch2) | (df['ch2'] == ch2)]
    df_node1 = df.loc[(df['ch1'] == ch1) | (df['ch2'] == ch1)]
    df_node2 = df.loc[(df['ch1'] == ch2) | (df['ch2'] == ch2)]
    links = df.values.tolist()
    node1 = [e for e in set(df_node1['ch1'].unique()) | set(df_node1['ch2'].unique()) if e not in (ch1, ch2)]
    node2 = [e for e in set(df_node2['ch1'].unique()) | set(df_node2['ch2'].unique()) if e not in (ch1, ch2)]
    node1.append([ch1, {'color': 'blue'}])
    node2.append([ch2, {'color': 'red'}])

    context = {'node1':node1, 'node2': node2, 'links': links}
    context.update(network_info(ch1, ch2))
    return context


def network_info(ch1, ch2):
    networkInfo = {}
    # G = nx.from_pandas_edgelist(df, source='ch1', target='ch2')
    G = nx.read_edgelist(DATA_URL + '/fanti.edgelist')
    networkInfo["nodesNum"] = G.number_of_nodes()
    networkInfo["edgesNum"] = G.number_of_edges()

    if ch2 != '':
        networkInfo["source"] = ch1
        networkInfo["target"] = ch2

        try:
            networkInfo["path"] = nx.shortest_path(G, source=ch1, target=ch2)
            networkInfo["shortestPath"] = '→'.join(nx.shortest_path(G, source=ch1, target=ch2))
        except (NetworkXNoPath, NodeNotFound):
            networkInfo["shortestPath"] = '不存在从<font size="3" color="red">%s</font>到达<font size="3" color="red">%s</font>的路径' % (ch1, ch2)
        try:
            networkInfo["shortestPathLength"] = nx.shortest_path_length(G, source=ch1, target=ch2)
        except (NetworkXNoPath, NodeNotFound):
            networkInfo["shortestPathLength"] = '不存在从<font size="3" color="red">%s</font>到达<font size="3" color="red">%s</font>的路径' % (ch1, ch2)
    else:
        networkInfo["source"] = ch1
        networkInfo["target"] = '-'
        networkInfo["shortestPath"] = '-'
        networkInfo["shortestPathLength"] = '-'
    return networkInfo


def checkIfExists(ch1='', ch2=''):
    """检查输入汉字是否已经存在于数据表中
    :param ch: str, 输入汉字
    :return: int
    :: ch2 为空
    1: ch1 在数据库中
    2: ch1 未在数据库中
    :: ch2 不为空
    3: ch1, ch2 都不在数据库中
    4: ch1, ch2 都在数据库中
    5: ch1 在数据库中, ch2 不在数据库中
    6: ch1 不在数据库中, ch2 在数据库中
    """
    # df = pd.read_csv(DATA_URL + '/chinese_characters.csv')
    df = pd.read_csv(DATA_URL + '/fanti.edgelist', sep='\t', header=None, names=['ch1', 'ch2'])
    all_char_unique = set(df.ch2.unique()) | set(df.ch1.unique())

    if ch2 == '':
        if ch1 not in all_char_unique:
            return 2
        else:
            return 1
    else:
        if ch1 not in all_char_unique and ch2 not in all_char_unique:
            return 3
        elif ch1 in all_char_unique and ch2 in all_char_unique:
            return 4
        elif ch1 in all_char_unique and ch2 not in all_char_unique:
            return 5
        elif ch1 not in all_char_unique and ch2 in all_char_unique:
            return 6


def plot_chnx_sample():
    df = pd.read_csv(DATA_URL + '/fanti.edgelist', sep='\t', header=None, names=['ch1', 'ch2'])
    df = df.head(100)
    df.drop_duplicates(keep='first', inplace=True)

    nodes = [{"name": ch, "symbolSize": 10} for ch in set(df['ch1'].unique()) | set(df['ch2'].unique())]
    links = [{"source": value[0], "target": value[1]} for value in df.values]
    graph = Graph("汉字-样例关系图", width=1200, height=600)
    graph.add("", nodes, links, repulsion=80, layout=None, graph_edge_length=150,
              is_roam=True, is_label_show=True, is_legend_show=True, draggable=False,
              lineStyle='-.', graph_edge_symbol=['circle', 'arrow'])
    graph.render()
    context = dict(
        myechart=graph.render_embed(),
        host='/static/js',
        script_list=graph.get_js_dependencies()
    )
    return context


def plot_chnx(ch1=None, ch2=None, check_code=None):
    # df = pd.read_csv(DATA_URL + '/chinese_characters.csv')
    df = pd.read_csv(DATA_URL + '/fanti.edgelist', sep='\t', header=None, names=['ch1', 'ch2'])
    df.drop_duplicates(keep='first', inplace=True)

    if check_code in [1, 5]:
        df = df.loc[(df['ch1'] == ch1) | (df['ch2'] == ch1)]
        nodes = [{"name": ch, "symbolSize": 10, "itemStyle": {"normal": {"color": 'red'}}}
                 for ch in set(df['ch1'].unique()) | set(df['ch2'].unique())]
        links = [{"source": value[0], "target": value[1], "lineStyle": {"normal": {"color": 'green'}}}
                 for value in df.values]
        graph = Graph("汉字-关系图", width=1200, height=600)
        graph.add("", nodes, links, repulsion=80, layout="force", graph_edge_length=150,
                  is_roam=True, is_label_show=True, is_legend_show=True, draggable=True,
                  lineStyle='-.', graph_edge_symbol=['circle', 'arrow'])
        graph.render()
    elif check_code == 4:
        df = df.loc[(df['ch1'] == ch1) | (df['ch2'] == ch1) | (df['ch1'] == ch2) | (df['ch2'] == ch2)]
        df1 = df.loc[((df['ch1'] == ch1) & (df['ch2'] != ch2)) | ((df['ch2'] == ch1) & (df['ch1'] != ch2))]
        df2 = df.loc[((df['ch1'] == ch2) & (df['ch2'] != ch1)) | ((df['ch2'] == ch2) & (df['ch1'] != ch1))]
        df3 = df.loc[((df['ch1'] == ch1) & (df['ch2'] == ch2)) | ((df['ch2'] == ch1) & (df['ch1'] == ch2))]

        nodes = [{"name": ch, "symbolSize": 10, "itemStyle": {"normal": {"color": 'red'}}}
                    for ch in set(df1['ch1'].unique()) | set(df1['ch2'].unique())]
        nodes += [{"name": ch, "symbolSize": 10, "itemStyle": {"normal": {"color": 'blue'}}}
                    for ch in set(df2['ch1'].unique()) | set(df2['ch2'].unique())]

        links = [{"source": value[0], "target": value[1], "lineStyle": {"normal": {"color": 'PaleTurquoise'}}}
                    for value in df1.values]
        links += [{"source": value[0], "target": value[1], "lineStyle": {"normal": {"color": 'gray'}}}
                    for value in df2.values]
        links += [{"source": value[0], "target": value[1], "lineStyle": {"normal": {"color": 'Teal'}}}
                  for value in df3.values]

        graph = Graph("汉字-关系图", width=1200, height=600)
        graph.add("", nodes, links, repulsion=80, layout="force", graph_edge_length=150,
                  is_roam=True, is_label_show=True, is_legend_show=True, draggable=True,
                  lineStyle='-.', graph_edge_symbol=['circle', 'arrow'])
        graph.render()

    elif check_code == 6:
        df = df.loc[(df['ch1'] == ch2) | (df['ch2'] == ch2)]
        nodes = [{"name": ch, "symbolSize": 10, "itemStyle": {"normal": {"color": 'red'}}}
                 for ch in set(df['ch1'].unique()) | set(df['ch2'].unique())]
        links = [{"source": value[0], "target": value[1], "lineStyle": {"normal": {"color": 'green'}}}
                 for value in df.values]
        graph = Graph("汉字-关系图", width=1200, height=600)
        graph.add("", nodes, links, repulsion=80, layout="force", graph_edge_length=150,
                  is_roam=True, is_label_show=True, is_legend_show=True, draggable=True,
                  lineStyle='-.', graph_edge_symbol=['circle', 'arrow'])
        graph.render()

    context = dict(
        myechart = graph.render_embed(),
        host='/static/js',
        script_list=graph.get_js_dependencies()
    )
    context.update(network_info(ch1, ch2))
    return context
