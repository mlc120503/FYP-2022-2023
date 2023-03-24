import networkx as nx
import matplotlib.pyplot as plt
from main import return_df
import seaborn as sns

# parameters of offset function for edge labels
rad = .1
connection_style = f'arc3,rad={rad}'


def offset(labels, position, distance=rad / 2, loop_shift=.2, aspect=1):
    for (a, b), object in labels.items():
        if a != b:
            edge_vector = distance * (position[b] - position[a])
            dx, dy = edge_vector[1] * aspect, -edge_vector[0] / aspect
            x, y = object.get_position()
            object.set_position((x + dx, y + dy))
        else:
            x, y = object.get_position()
            object.set_position((x, y + loop_shift))


def subtraction(a, b):
    return a - b


def get_aspect(ax):
    figure_w, figure_h = ax.get_figure().get_size_inches()
    _, _, w, h = ax.get_position().bounds
    disp_ratio = (figure_h * h) / (figure_w * w)
    data_ratio = subtraction(*ax.get_ylim()) / subtraction(*ax.get_xlim())

    return disp_ratio / data_ratio


def flowingGraph():
    # import the dataframe
    df = return_df()

    plt.figure(figsize=(15, 8))
    G = nx.from_pandas_edgelist(df, source='grad',
                                target='work', edge_attr='count',
                                create_using=nx.DiGraph())
    #G.remove_node('Others')
    weight = nx.get_edge_attributes(G, 'count')
    pos = nx.shell_layout(G, scale=1)
    nx.draw_networkx_nodes(G, pos, node_size=300, node_color='lightblue')
    nx.draw_networkx_labels(G, pos=pos, font_color='red')
    nx.draw_networkx_edges(G, pos=pos, edgelist=G.edges(), edge_color='black',
                           connectionstyle=connection_style)
    label = nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=weight)
    offset(label, pos, aspect=get_aspect(plt.gca()))


def heatmap():
    # import the dataframe
    df = return_df()

    df = df[df['grad'] != 'Others']
    df = df[df['grad'] != df['work']]
    #y_order = ['CUHK', 'CityU', 'HKU', 'HKUST', 'PolyU']
    y_order = ['CUHK', 'CityU', 'HKU', 'HKUST', 'PolyU', 'Toronto', 'Stanford', 'NUS', 'MIT', 'Columbia']
    #y_order = ['CUHK', 'CityU', 'HKU', 'HKUST', 'PolyU', 'Stanford', 'NUS', 'MIT', 'Others']
    matrix = df.pivot('grad', 'work', 'count').reindex(y_order)

    plt.figure(figsize=(10, 8))
    sns.heatmap(matrix, annot=True, cmap='Reds')
    plt.xlabel('Workplace')
    plt.ylabel('Graduated from')
    plt.yticks(rotation=20)


flowingGraph()
heatmap()
plt.show()
