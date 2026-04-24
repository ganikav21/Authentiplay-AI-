import networkx as nx

def build_graph(videos, similarity_map):

    G = nx.DiGraph()

    videos = sorted(videos, key=lambda x: x["published_at"])

    for v in videos:
        G.add_node(v["channel"])

    for i in range(len(videos)):
        for j in range(i+1, len(videos)):

            v1 = videos[i]
            v2 = videos[j]

            key = (v1["video_id"], v2["video_id"])

            if key in similarity_map and similarity_map[key] > 50:
                G.add_edge(
                    v1["channel"],
                    v2["channel"],
                    weight=similarity_map[key]
                )

    return G


def detect_source(G):
    scores = dict(G.out_degree())
    if not scores:
        return None
    return max(scores, key=scores.get)