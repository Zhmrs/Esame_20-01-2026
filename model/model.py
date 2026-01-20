import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._artists_list = []
        self.id_map_artist={}
        self._album_artist=[]
        self.load_all_artists()

        self._nodes=[]

    def load_all_artists(self):
        self._artists_list = DAO.get_all_artists()
        print(f"Artisti: {self._artists_list}")
        for artist in self._artists_list:
            self.id_map_artist[artist.id] = artist

    def load_artists_with_min_albums(self, min_albums):
        self._album_artist=DAO.get_albums_artist(min_albums)

    def build_graph(self):
        self._graph.clear()
        self._nodes=[]

        for a in self._album_artist:
            for artist in self._artists_list:
                if artist.name == a[1] and artist.id == a[0]:
                    self._nodes.append(artist)

        self._graph.add_nodes_from(self._nodes)

        edges=[]
        self._edges=DAO.get_connessione(self._nodes)
        for a in self._edges:
            if self.id_map_artist[a[0]] and self.id_map_artist[a[1]]:
                edges.append((self.id_map_artist[a[0]], self.id_map_artist[a[1]], a[2]))

        self._graph.add_weighted_edges_from(self._edges)

    def numero_nodi(self):
        return len(self._graph.nodes)


    def numero_archi(self):
        return len(self._graph.edges)
