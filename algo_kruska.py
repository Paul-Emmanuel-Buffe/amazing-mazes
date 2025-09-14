class UnionFind:
    # structure union find pour gérer des ensembles disjoints
    # permet de vérifier rapidement si deux sommets sont connectés
    def __init__(self, n):
        # initialisation avec n sommets chacun dans son propre ensemble
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x):
        # retourne la racine de l ensemble contenant x
        # applique la compression de chemin
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        # fusionne les ensembles de x et y
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        # union par rang pour garder des arbres équilibrés
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        self.components -= 1
        return True

    def same_set(self, x, y):
        # retourne vrai si x et y sont dans le même ensemble
        return self.find(x) == self.find(y)

    def get_components(self):
        # retourne le nombre de composantes restantes
        return self.components


class KruskalGraph:
    # graphe représenté par une liste d arêtes
    def __init__(self, vertices):
        # initialisation avec un nombre donné de sommets
        self.V = vertices
        self.edges = []

    def add_edge(self, u, v, weight):
        # ajoute une arête entre u et v avec un poids
        self.edges.append([u, v, weight])

    def kruskal_mst(self):
        # applique l algorithme de kruskal pour trouver un acm
        self.edges.sort(key=lambda edge: edge[2])  # tri des arêtes par poids

        uf = UnionFind(self.V)
        mst_edges = []
        total_weight = 0
        edges_added = 0

        for u, v, weight in self.edges:
            if not uf.same_set(u, v):
                mst_edges.append([u, v, weight])
                total_weight += weight
                edges_added += 1
                uf.union(u, v)
                if edges_added == self.V - 1:
                    break

        return mst_edges, total_weight





                  


       

       
              

       
       