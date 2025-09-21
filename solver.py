import heapq
import os
from PIL import Image
from solver_metric import SolverMetricsLogger

class Solver:
    def __init__(self, labyrinthe, depart, sortie):
        self.labyrinthe = [list(row) for row in labyrinthe]
        self.n = len(labyrinthe)
        self.m = len(labyrinthe[0])
        self.depart = depart
        self.sortie = sortie

    def _voisins(self, x, y):
        """Retourne les voisins accessibles (cases vides)."""
        deplacements = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        for dx, dy in deplacements:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < self.n
                and 0 <= ny < self.m
                and self.labyrinthe[nx][ny] == "."
            ):
                yield nx, ny

    def _mark_solution(self, chemin, explored):
        """Retourne une version du labyrinthe avec o/*/S/E marqués."""
        lab_mod = [row[:] for row in self.labyrinthe]
        for (x, y) in explored:
            if (x, y) not in chemin and lab_mod[x][y] == ".":
                lab_mod[x][y] = "*"
        for (x, y) in chemin:
            lab_mod[x][y] = "o"
        lab_mod[self.depart[0]][self.depart[1]] = "S"
        lab_mod[self.sortie[0]][self.sortie[1]] = "E"
        return ["".join(row) for row in lab_mod]

    def solve_astar(self, logger=None):
        start, goal = self.depart, self.sortie
        def heuristique(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan
        open_set = []
        heapq.heappush(open_set, (heuristique(start, goal), 0, start))
        came_from = {}
        g_score = {start: 0}
        explored = set()
        while open_set:
            _, cost, current = heapq.heappop(open_set)
            if logger:
                logger.increment_nodes()
            if current == goal:
                chemin = []
                while current in came_from:
                    chemin.append(current)
                    current = came_from[current]
                chemin.append(start)
                chemin.reverse()
                if logger:
                    logger.set_path_length(len(chemin))
                return self._mark_solution(chemin, explored), chemin
            explored.add(current)
            for voisin in self._voisins(*current):
                tentative_g = cost + 1
                if voisin not in g_score or tentative_g < g_score[voisin]:
                    g_score[voisin] = tentative_g
                    f = tentative_g + heuristique(voisin, goal)
                    heapq.heappush(open_set, (f, tentative_g, voisin))
                    came_from[voisin] = current
        return None, None

    def to_image(self, labyrinthe_solution, pixel_size=1, output_file="solution.jpg"):
        n = len(labyrinthe_solution)
        m = len(labyrinthe_solution[0])
        img = Image.new("RGB", (m * pixel_size, n * pixel_size), "white")
        pixels = img.load()
        couleurs = {
            "#": (0, 0, 0),
            ".": (255, 255, 255),
            "o": (0, 255, 0),
            "*": (100, 100, 100),
            "S": (0, 0, 255),
            "E": (255, 0, 0),
        }
        for i, row in enumerate(labyrinthe_solution):
            for j, cell in enumerate(row):
                couleur = couleurs.get(cell, (255, 255, 255))
                for dx in range(pixel_size):
                    for dy in range(pixel_size):
                        pixels[j * pixel_size + dx, i * pixel_size + dy] = couleur
        img.save(output_file)
        print(f"Image enregistrée sous : {output_file}")

def run_automated_solving():
    """Résout uniquement le labyrinthe kruskal_strict_1000_26.txt avec A* et génère une image."""
    maze_directory = r"C:\Users\Windows\Desktop\projets\2a\amazing-mazes\kuskal_grids"
    pictures_directory = r"C:\Users\Windows\Desktop\projets\2a\amazing-mazes\pictures"
    csv_path = r"C:\Users\Windows\Desktop\projets\2a\amazing-mazes\solver_metrics.csv"
    maze_file = os.path.join(maze_directory, "kruskal_strict_5000_7.txt")

    # Créer le dossier pictures s'il n'existe pas
    if not os.path.exists(pictures_directory):
        os.makedirs(pictures_directory)
        print(f"Dossier créé : {pictures_directory}")

    print(f"Vérification du fichier : {maze_file}")
    if not os.path.exists(maze_file):
        print(f"ERREUR : Le fichier {maze_file} n'existe pas !")
        return

    logger = SolverMetricsLogger(csv_file=csv_path)

    print(f"Traitement du fichier : {os.path.basename(maze_file)} (A*)")
    try:
        with open(maze_file, "r") as f:
            labyrinthe = [line.strip() for line in f.readlines()]
            n = (len(labyrinthe) - 1) // 2
            depart = (0, 1)
            sortie = (2 * n, 2 * n - 1)
            print(f"Labyrinthe chargé : {len(labyrinthe)} lignes, départ={depart}, sortie={sortie}")

        solver = Solver(labyrinthe, depart, sortie)
        logger.start(
            maze_name=os.path.basename(maze_file),
            maze_size=f"{solver.n}x{solver.m}",
            algorithm="astar",
        )

        solution, chemin = solver.solve_astar(logger=logger)
        if solution:
            logger.stop(maze_file)
            print(f"Solution trouvée : Nœuds explorés = {logger.nodes_explored}, Longueur chemin = {logger.path_length}")

            # Générer l'image avec une taille de pixel réduite
            output_image_path = os.path.join(pictures_directory, f"solution_{os.path.basename(maze_file)}.jpg")
            solver.to_image(solution, pixel_size=1, output_file=output_image_path)

            # Vérifier que l'image a bien été enregistrée
            if os.path.exists(output_image_path):
                print(f"✅ Image enregistrée avec succès : {output_image_path}")
            else:
                print(f"❌ Échec de l'enregistrement de l'image : {output_image_path}")
        else:
            print("Aucun chemin trouvé avec A*")
            logger.stop(maze_file)

    except Exception as e:
        print(f"Erreur lors du traitement du fichier {maze_file} : {e}")

    print(f"\nTraitement terminé. Fichier CSV des métriques sauvegardé dans : {csv_path}")

if __name__ == "__main__":
    run_automated_solving()



