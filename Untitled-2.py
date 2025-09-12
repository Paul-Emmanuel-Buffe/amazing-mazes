class UnionFind:
    """
    Structure de données Union-Find (Disjoints Sets)
    
    Cette structure nous permet de :
    1. Grouper les sommets en composantes connexes
    2. Vérifier rapidement si deux sommets sont dans la même composante
    3. Fusionner deux composantes efficacement
    """

    def __init__(self, n):
        """
        Initialise n éléments, chacun dans son propre ensemble
        
        Args:
            n: nombre d'éléments (sommets)
        """

        # parent[i] = parent du sommet i dans l'arbre Union-Find
        self.parent = list(range(n))  

        # rank[i] = hauteur approximative de l'arbre enraciné en i
        self.rank = [0] * n

        # Nombre de composantes connexes
        self.components = n
        
        print(f"🔧 Initialisation Union-Find pour {n} sommets")
        print(f"   Parent initial : {self.parent}")
        print(f"   Rang initial   : {self.rank}")
        print(f"   Composantes    : {self.components}")
        print()

    def find(self, x): 
                """
            Trouve le représentant (racine) de l'ensemble contenant x
            
            Utilise la compression de chemin pour optimiser les recherches futures.
            
            Args:
                x: élément dont on cherche le représentant
                
            Returns:
                Le représentant de l'ensemble contenant x
            """
            
                if self.parent[x] != x:
                    # Compression de chemin : on fait pointer x directement vers la racine
                    original_parent = self.parent[x]
                    self.parent[x] = self.find(self.parent[x])
                    print(f"    🔍 Compression de chemin : {x} pointait vers {original_parent}, maintenant vers {self.parent[x]}")
                return self.parent[x]

    def union(self, x, y):
                """
                Unit les ensembles contenant x et y
                
                Utilise l'union par rang pour maintenir les arbres équilibrés.
                
                Args:
                    x, y: éléments dont on veut unir les ensembles
                    
                Returns:
                    True si les ensembles ont été unis, False s'ils étaient déjà dans le même ensemble
                """
            
                root_x = self.find(x)
                root_y = self.find(y)

                # Déjà dans le même ensemble
                if root_x == root_y:
                    print(f"    ❌ {x} et {y} sont déjà dans la même composante (racine {root_x})") 
                    return False

                print(f"    🔗 Union de {x} (racine {root_x}) et {y} (racine {root_y})")
        
                # Union par rang : attache l'arbre plus petit sous l'arbre plus grand
                if  self.rank[root_x] < self.rank[root_y]:
                    self.parent[root_x] = root_y
                    print(f"       Arbre {root_x} (rang {self.rank[root_x]}) attaché sous {root_y} (rang {self.rank[root_y]})")

                elif self.rank[root_x] > self.rank[root_y]:
                    self.parent[root_y] = root_x
                    print(f"       Arbre {root_y} (rang {self.rank[root_y]}) attaché sous {root_x} (rang {self.rank[root_x]})")

                else:
                    # Rangs égaux : on choisit une racine et on augmente son rang
                    self.parent[root_y] = root_x 
                    self.rank[root_x] += 1
                    print(f"       Rangs égaux : {root_y} attaché sous {root_x}, nouveau rang de {root_x} = {self.rank[root_x]}") 

                self.components -= 1
                print(f"       Nouvelles composantes : {self.components}")
                return True

    def same_set(self, x, y):
        # vérifie si x et y sont dans le même ensemble
        return self.find(x) == self.find(y)

    def get_components(self):
        # retourne le nombre de composantes connexes
        return self.components
class KruskalGraph:
    def __init__(self, vertices): 
            """
            Initialise un graphe avec le nombre spécifié de sommets
            
            Args:
                vertices: nombre de sommets dans le graphe
            """
            self.V = vertices 
            self.edges = [] # Liste des arrêtes

            print(f"📊 Création d'un graphe avec {vertices} sommets")
            print()

    def add_edge(self, u, v, weight):
        """
            Ajoute une arête au graphe
            
            Args:
                u, v: sommets de l'arête
                weight: poids de l'arête
            """
        self.edges.append([u, v, weight])
        print(f"➕ Arête ajoutée : {u} - {v} (poids {weight})")

    def print_graph(self):
        """Affiche toutes les arêtes du graphe"""
        print("📋 Arêtes du graphe :")

        for i, (u, v, weight) in enumerate(self.edges):
            print(f"  {i+1}.  {u} - {v} : {weight}")
        print()

    def kruskal_mst(self):
        """
            Applique l'algorithme de Kruskal pour trouver l'Arbre Couvrant Minimal
            
            Returns:
                Liste des arêtes de l'ACM et le poids total
            """
        print("🚀 DÉBUT DE L'ALGORITHME DE KRUSKAL")
        print("=" * 50)

        # ÉTAPE 1 : Trier les arêtes par poids croissant
        print("📑 ÉTAPE 1 : Tri des arêtes par poids croissant")
        print("   Arêtes avant tri :")
        for u, v, weight in self.edges:
                print(f"     {u} - {v} : {weight}")
            # Tri des arêtes (algorithme glouton : on veut les plus légères en premier)
        self.edges.sort(key=lambda edge: edge[2])

        print("\n   Arêtes après tri :")
        for i, (u, v, weight) in enumerate(self.edges):
                print(f"     {i+1}. {u} - {v} : {weight}")
        print()
            
            # ÉTAPE 2 : Initialiser la structure Union-Find
        print("🔧 ÉTAPE 2 : Initialisation de Union-Find")
        uf = UnionFind(self.V)

        # ÉTAPE 3 : Traiter chaque arête
        print("🔍 ÉTAPE 3 : Traitement des arêtes")
        print("   Règle : Ajouter l'arête seulement si elle ne crée pas de cycle")
        print()

        mst_edges= [] # Arêtes de l'Arbre Couvrant Minimal
        total_weight = 0
        edges_added = 0

        for i, (u, v, weight) in enumerate(self.edges):
                print(f"🎯 Examen de l'arête {i+1}/{len(self.edges)} : {u} - {v} (poids {weight})")

                # Vérifier si les sommets sont dans la même composante
                if not uf.same_set(u, v):
                    # Pas de cycle : on peut ajouter cette arête
                    print(f"   ✅ ACCEPTÉE : {u} et {v} sont dans des composantes différentes")

                    mst_edges.append([u, v, weight])
                    total_weight += weight 
                    edges_added +=1

                    # Unir les composantes
                    uf.union(u,v)

                    print(f"   📊 Progression : {edges_added}/{self.V-1} arêtes ajoutées")

                    # Condition d'arrêt : on a n-1 arêtes (arbre complet)
                    if edges_added == self.V-1:
                            print(f"   🎉 Arbre complet ! {self.V-1} arêtes ajoutées pour {self.V} sommets")
                            break
                else:
                            # Cycle détecté : on rejette cette arête
                        print(f"   ❌ REJETÉE : {u} et {v} sont dans la même composante (créerait un cycle)")
                
                print()

                print("🏆 RÉSULTAT FINAL")
        print("=" * 50)
        print("🌳 Arbre Couvrant Minimal trouvé :")
        
        for i, (u, v, weight) in enumerate(mst_edges):
            print(f"   {i+1}. {u} - {v} : {weight}")
        
        print(f"\n💰 Poids total de l'ACM : {total_weight}")
        print(f"📊 Nombre d'arêtes : {len(mst_edges)} (pour {self.V} sommets)")
        
        return mst_edges, total_weight


# ====================
# EXEMPLE PRATIQUE
# ====================

def exemple_cours():
    """Exemple détaillé avec le graphe de l'étudiant"""
    
    print("🎓 EXEMPLE PRATIQUE : Votre graphe de l'exercice")
    print("=" * 60)
    
    # Création du graphe (7 sommets)
    # A=0, B=1, C=2, D=3, E=4, F=5, G=6
    g = KruskalGraph(7)
    
    print("📍 Correspondance des sommets :")
    print("   A=0, B=1, C=2, D=3, E=4, F=5, G=6")
    print()
    
    # Ajout des arêtes de votre exemple
    g.add_edge(3, 1, 1)   # D-B : 1
    g.add_edge(5, 6, 1)   # F-G : 1  
    g.add_edge(0, 1, 2)   # A-B : 2
    g.add_edge(3, 4, 2)   # D-E : 2
    g.add_edge(1, 4, 3)   # B-E : 3
    g.add_edge(0, 3, 4)   # A-D : 4
    g.add_edge(0, 5, 5)   # A-F : 5
    g.add_edge(6, 2, 6)   # G-C : 6
    g.add_edge(1, 2, 7)   # B-C : 7
    g.add_edge(1, 6, 7)   # B-G : 7
    g.add_edge(5, 1, 8)   # F-B : 8
    g.add_edge(4, 2, 10)  # E-C : 10
    
    print()
    
    # Application de l'algorithme
    mst_edges, total_weight = g.kruskal_mst()
    
    print(f"\n🎯 Comparaison avec votre travail manuel :")
    print("   Votre sélection : DB(1), FG(1), AB(2), DE(2), AF(5)")
    print("   Résultat Kruskal :", end=" ")
    for u, v, w in mst_edges:
        # Conversion des indices vers les lettres
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        print(f"{letters[u]}{letters[v]}({w})", end=", " if (u,v,w) != mst_edges[-1] else "")
    print()


def exemple_simple():
    """Exemple simple pour bien comprendre"""
    
    print("\n" + "="*60)
    print("🔰 EXEMPLE SIMPLE pour débuter")
    print("="*60)
    
    # Graphe simple : triangle avec une arête supplémentaire
    g = KruskalGraph(4)  # 4 sommets : 0, 1, 2, 3
    
    g.add_edge(0, 1, 1)   # 0-1 : 1
    g.add_edge(1, 2, 2)   # 1-2 : 2  
    g.add_edge(0, 2, 3)   # 0-2 : 3 (cette arête créera un cycle)
    g.add_edge(2, 3, 4)   # 2-3 : 4
    
    print()
    mst_edges, total_weight = g.kruskal_mst()


if __name__ == "__main__":
    # Lancer l'exemple principal
    exemple_cours()
    
    # Lancer l'exemple simple
    exemple_simple()
    
    print("\n🎓 Félicitations ! Vous avez maintenant une compréhension complète de l'algorithme de Kruskal.")
    print("💡 Exercice : Essayez de créer votre propre graphe et d'appliquer l'algorithme !")




                  


       

       
              

       
       