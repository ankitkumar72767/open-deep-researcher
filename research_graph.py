import networkx as nx
import plotly.graph_objects as go


def create_research_graph(
    topic,
    keywords
):

    G = nx.Graph()

    # Main Topic Node
    G.add_node(topic)

    # Dynamic Keywords from Graph Agent
    for item in keywords:

        if item.strip():

            G.add_node(item)

            G.add_edge(
                topic,
                item
            )

    # Graph Layout
    pos = nx.spring_layout(
        G,
        seed=42,
        k=1.2
    )

    # Edges
    edge_x = []
    edge_y = []

    for edge in G.edges():

        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]

        edge_x.extend(
            [x0, x1, None]
        )

        edge_y.extend(
            [y0, y1, None]
        )

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        hoverinfo="none",
        line=dict(
            width=2
        )
    )

    # Nodes
    node_x = []
    node_y = []

    for node in G.nodes():

        x, y = pos[node]

        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=list(G.nodes()),
        textposition="top center",
        hoverinfo="text",
        marker=dict(
            size=35
        )
    )

    # Figure
    fig = go.Figure(
        data=[
            edge_trace,
            node_trace
        ]
    )

    fig.update_layout(
        title=f"Research Knowledge Graph: {topic}",
        showlegend=False,
        hovermode="closest",
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            visible=False
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            visible=False
        ),
        height=600
    )

    return fig