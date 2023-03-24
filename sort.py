import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from main import return_df

# import the dataframe
df = return_df()

# 創建一個networkx directed graph
G = nx.DiGraph()

# 將所有大學加入圖表
for uni in set(df['grad']).union(set(df['work'])):
    G.add_node(uni)

# 將所有流動情況加入圖表
for index, row in df.iterrows():
    if row['count'] > df.loc[(df['grad'] == row['work']) & (df['work'] == row['grad']), 'count'].values.size > 0 and \
            row['count'] > df.loc[(df['grad'] == row['work']) & (df['work'] == row['grad']), 'count'].values[0]:
        G.add_edge(row['grad'], row['work'])
    elif row['count'] < df.loc[(df['grad'] == row['work']) & (df['work'] == row['grad']), 'count'].values.size > 0 and \
            row['count'] < df.loc[(df['grad'] == row['work']) & (df['work'] == row['grad']), 'count'].values[0]:
        G.add_edge(row['work'], row['grad'])

# 使用networkx中的spring_layout()布局算法調整節點的位置
pos = nx.spring_layout(G, k=50, iterations=500)

# 使用networkx和matplotlib繪製圖表
G.remove_node('Others')
print(G)
nx.draw_networkx_nodes(G, pos, node_size=400)
nx.draw_networkx_edges(G, pos, edge_color='black', arrowsize=10)
nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
topological_order = list(nx.topological_sort(G))
print("全局次序：", topological_order)
plt.axis('off')
plt.show()
